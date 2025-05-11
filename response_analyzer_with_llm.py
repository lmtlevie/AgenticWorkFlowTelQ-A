#!/usr/bin/env python
"""
Script para analizar críticamente las respuestas generadas por el sistema multi-agente
utilizando LLMs para evaluar cada criterio
"""
import argparse
import logging
import os
import re
import json
from typing import Dict, Any, List, Optional

from model_provider import OllamaModel

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Criterios de análisis
ANALYSIS_CRITERIA = [
    "completitud", 
    "precision_tecnica", 
    "estructura_claridad", 
    "fuentes", 
    "limitaciones_desafios", 
    "sesgos", 
    "profundidad"
]

# Descripción de los criterios
CRITERIA_DESCRIPTIONS = {
    "completitud": "¿Es completa? ¿Faltan aspectos importantes?",
    "precision_tecnica": "¿Es precisa? ¿Hay errores conceptuales o técnicos?",
    "estructura_claridad": "¿Está bien estructurada y es clara?",
    "fuentes": "¿Cita fuentes o se basa en conocimiento general? (Verificar la plausibilidad)",
    "limitaciones_desafios": "¿Identifica limitaciones, desafíos o trade-offs?",
    "sesgos": "¿Presenta algún sesgo obvio?",
    "profundidad": "¿Qué tan profunda es la respuesta? ¿Se queda en la superficie o entra en detalles relevantes?"
}

def load_response(input_file: str) -> Dict[str, Any]:
    """
    Carga y analiza un archivo de resumen de respuestas
    
    Args:
        input_file: Ruta al archivo de resumen
        
    Returns:
        Diccionario con las preguntas y respuestas analizadas
    """
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Dividir por preguntas (separadas por ---)
        sections = content.split("---")
        
        results = {}
        for section in sections:
            if not section.strip():
                continue
                
            # Encontrar el título de la sección
            section_title_match = re.search(r"## ([^\n]+)", section)
            if not section_title_match:
                continue
                
            section_title = section_title_match.group(1).strip().lower().replace(" ", "_")
            
            # Extraer pregunta
            question_match = re.search(r"### Pregunta\s*\n\s*\n(.*?)\n\s*\n", section, re.DOTALL)
            question = question_match.group(1) if question_match else ""
            
            # Extraer respuesta del experto
            expert_match = re.search(r"### Respuesta del Experto\s*\n\s*\n(.*?)\n\s*\n", section, re.DOTALL)
            expert_response = expert_match.group(1) if expert_match else ""
            
            # Extraer análisis del crítico
            critic_match = re.search(r"### Análisis del Crítico\s*\n\s*\n(.*?)\n\s*\n", section, re.DOTALL)
            critic_analysis = critic_match.group(1) if critic_match else ""
            
            # Extraer análisis final
            final_match = re.search(r"### Análisis Final\s*\n\s*\n(.*?)(?:\n\s*\n|$)", section, re.DOTALL)
            final_analysis = final_match.group(1) if final_match else ""
            
            results[section_title] = {
                "question": question,
                "expert_response": expert_response,
                "critic_analysis": critic_analysis,
                "final_analysis": final_analysis
            }
        
        return results
    
    except Exception as e:
        logger.error(f"Error loading responses: {e}")
        return {}

def evaluate_criterion(model: OllamaModel, criterion: str, question: str, response: str) -> Dict[str, Any]:
    """
    Evalúa un criterio específico usando un modelo LLM
    
    Args:
        model: Modelo LLM a utilizar
        criterion: Criterio a evaluar
        question: Pregunta original
        response: Respuesta a evaluar
        
    Returns:
        Evaluación del criterio con puntuación y comentarios
    """
    prompt = f"""
INSTRUCCIÓN: RESPONDE COMPLETAMENTE EN ESPAÑOL.

Evalúa la siguiente respuesta según el criterio de {criterion}: {CRITERIA_DESCRIPTIONS[criterion]}

PREGUNTA:
{question}

RESPUESTA:
{response}

Evalúa la respuesta en una escala del 1 al 10, donde 10 es excelente. 
Proporciona comentarios detallados EN ESPAÑOL que justifiquen tu puntuación.

Responde en formato JSON siguiendo exactamente esta estructura:
{{
  "score": [puntuación del 1-10],
  "comments": "[comentarios detallados EN ESPAÑOL]"
}}

IMPORTANTE: Todo el contenido debe estar en español, incluyendo los comentarios.
"""
    
    try:
        # Utilizar el modelo para evaluar
        llm_response = model.generate(prompt, role="Evaluador de Respuestas", max_tokens=1000)
        
        # Extraer el JSON de la respuesta
        json_match = re.search(r"```json\s*(.*?)\s*```", llm_response, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Intentar encontrar el JSON sin formato de código
            json_match = re.search(r"({.*})", llm_response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                json_str = llm_response
        
        # Limpiar el string de JSON
        json_str = json_str.strip()
        
        # Parsear el JSON
        result = json.loads(json_str)
        
        # Asegurar que tenga los campos necesarios
        if "score" not in result or "comments" not in result:
            raise ValueError("La respuesta no contiene los campos requeridos (score, comments)")
        
        return result
    
    except Exception as e:
        logger.error(f"Error evaluando criterio {criterion}: {e}")
        return {
            "score": 0,
            "comments": f"Error al evaluar: {str(e)}"
        }

def analyze_response_with_llm(model: OllamaModel, question_key: str, response_data: Dict[str, str]) -> Dict[str, Any]:
    """
    Analiza críticamente una respuesta según los criterios usando un modelo LLM
    
    Args:
        model: Modelo LLM a utilizar
        question_key: Clave de la pregunta
        response_data: Datos de la respuesta (question, expert_response, etc.)
        
    Returns:
        Análisis crítico de la respuesta
    """
    question = response_data.get("question", "")
    expert_response = response_data.get("expert_response", "")
    
    # Evaluar cada criterio
    analysis = {}
    for criterion in ANALYSIS_CRITERIA:
        logger.info(f"Evaluando criterio: {criterion}")
        analysis[criterion] = evaluate_criterion(model, criterion, question, expert_response)
    
    # Calcular puntuación total
    total_score = sum(item["score"] for item in analysis.values()) / len(analysis)
    
    # Generar recomendaciones para mejorar
    recommendations_prompt = f"""
INSTRUCCIÓN: RESPONDE COMPLETAMENTE EN ESPAÑOL.

Basándote en el siguiente análisis de una respuesta, proporciona recomendaciones específicas para mejorarla:

PREGUNTA:
{question}

RESPUESTA:
{expert_response}

ANÁLISIS:
{json.dumps(analysis, indent=2, ensure_ascii=False)}

Proporciona recomendaciones concretas para mejorar la respuesta en cada uno de los criterios que tengan puntuaciones bajas.
Asegúrate de responder COMPLETAMENTE EN ESPAÑOL.
"""
    
    recommendations = model.generate(recommendations_prompt, role="Evaluador de Respuestas en Español", max_tokens=1000)
    
    # Generar respuesta mejorada
    improved_response_prompt = f"""
INSTRUCCIÓN: RESPONDE COMPLETAMENTE EN ESPAÑOL.

Mejora la siguiente respuesta basándote en el análisis crítico proporcionado:

PREGUNTA:
{question}

RESPUESTA ORIGINAL:
{expert_response}

ANÁLISIS CRÍTICO:
{json.dumps(analysis, indent=2, ensure_ascii=False)}

RECOMENDACIONES:
{recommendations}

Genera una versión mejorada completa de la respuesta que corrija los problemas identificados y añada profundidad donde sea necesario.
La respuesta debe estar COMPLETAMENTE EN ESPAÑOL.
"""
    
    improved_response = model.generate(improved_response_prompt, role="Experto en Telecomunicaciones", max_tokens=1500)
    
    # Generar reflexión sobre el proceso
    reflection_prompt = f"""
INSTRUCCIÓN: RESPONDE COMPLETAMENTE EN ESPAÑOL.

Reflexiona sobre la utilidad de la IA en la generación de la siguiente respuesta:

PREGUNTA:
{question}

RESPUESTA ORIGINAL:
{expert_response}

ANÁLISIS CRÍTICO:
{json.dumps(analysis, indent=2, ensure_ascii=False)}

Reflexiona sobre:
1. ¿Qué tan útil fue la IA en esta respuesta?
2. ¿Dónde falló?
3. ¿Qué tipo de aspectos de la pregunta manejó mejor/peor?

Asegúrate de responder COMPLETAMENTE EN ESPAÑOL.
"""
    
    reflection = model.generate(reflection_prompt, role="Analista de IA", max_tokens=1000)
    
    return {
        "question_key": question_key,
        "analysis": analysis,
        "total_score": total_score,
        "recommendations": recommendations,
        "improved_response": improved_response,
        "reflection": reflection
    }

def generate_report(analyses: Dict[str, Any], output_file: str):
    """
    Genera un informe con los análisis críticos
    
    Args:
        analyses: Diccionario con los análisis por pregunta
        output_file: Ruta al archivo de salida
    """
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# ANÁLISIS CRÍTICO DE RESPUESTAS\n\n")
        
        for question_key, analysis_data in analyses.items():
            f.write(f"## {question_key.upper().replace('_', ' ')}\n\n")
            
            f.write("### Evaluación por criterios\n\n")
            f.write("| Criterio | Puntuación | Comentarios |\n")
            f.write("|----------|------------|-------------|\n")
            
            for criterion, data in analysis_data["analysis"].items():
                criterion_desc = CRITERIA_DESCRIPTIONS.get(criterion, criterion)
                f.write(f"| **{criterion_desc}** | {data['score']}/10 | {data['comments']} |\n")
            
            f.write(f"\n**Puntuación total**: {analysis_data['total_score']:.1f}/10\n\n")
            
            f.write("### Recomendaciones para mejorar\n\n")
            f.write(f"{analysis_data['recommendations']}\n\n")
            
            f.write("### Respuesta mejorada\n\n")
            f.write(f"{analysis_data['improved_response']}\n\n")
            
            f.write("### Reflexión sobre el proceso\n\n")
            f.write(f"{analysis_data['reflection']}\n\n")
            
            f.write("---\n\n")

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Analiza críticamente las respuestas del sistema multi-agente usando LLM")
    parser.add_argument(
        "--input", 
        type=str, 
        default="./outputs/resumen_respuestas.txt",
        help="Archivo de entrada con las respuestas a analizar"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default="./outputs/analisis_critico_llm.md",
        help="Archivo de salida con el análisis crítico"
    )
    parser.add_argument(
        "--question", 
        type=str, 
        default=None,
        help="Clave específica de pregunta a analizar (por defecto, todas)"
    )
    parser.add_argument(
        "--ollama-model", 
        type=str, 
        default="deepseek-coder:33b",
        help="Modelo de Ollama para análisis (default: deepseek-coder:33b)"
    )
    parser.add_argument(
        "--ollama-api", 
        type=str, 
        default="http://localhost:11434",
        help="URL base de la API de Ollama"
    )
    return parser.parse_args()

def main():
    """Función principal"""
    args = parse_args()
    
    # Verificar que exista el archivo de entrada
    if not os.path.exists(args.input):
        logger.error(f"El archivo de entrada no existe: {args.input}")
        return
    
    # Crear directorio de salida si no existe
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Inicializar modelo LLM
    model = OllamaModel(model_name=args.ollama_model, api_base=args.ollama_api)
    logger.info(f"Utilizando modelo LLM: {args.ollama_model}")
    
    # Cargar respuestas
    responses = load_response(args.input)
    if not responses:
        logger.error("No se encontraron respuestas para analizar.")
        return
    
    logger.info(f"Se encontraron {len(responses)} respuestas para analizar.")
    
    # Filtrar por pregunta específica si se proporciona
    if args.question and args.question in responses:
        responses = {args.question: responses[args.question]}
    
    # Analizar respuestas
    analyses = {}
    for question_key, response_data in responses.items():
        logger.info(f"Analizando respuesta para: {question_key}")
        analyses[question_key] = analyze_response_with_llm(model, question_key, response_data)
    
    # Generar informe
    generate_report(analyses, args.output)
    logger.info(f"Informe generado: {args.output}")

if __name__ == "__main__":
    main() 