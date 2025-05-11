#!/usr/bin/env python
"""
Script para analizar críticamente las respuestas generadas por el sistema multi-agente
"""
import argparse
import logging
import os
import re
from typing import Dict, Any, List, Optional

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

def analyze_response(question_key: str, response_data: Dict[str, str]) -> Dict[str, Any]:
    """
    Analiza críticamente una respuesta según los criterios
    
    Args:
        question_key: Clave de la pregunta
        response_data: Datos de la respuesta (question, expert_response, etc.)
        
    Returns:
        Análisis crítico de la respuesta
    """
    # Aquí normalmente usaríamos un LLM para analizar la respuesta
    # En este ejemplo, generamos un análisis de muestra
    
    expert_response = response_data.get("expert_response", "")
    
    # En un sistema real, aquí llamaríamos al modelo para evaluar cada criterio
    analysis = {
        "completitud": {
            "score": 0, # 0-10, donde 10 es completamente completo
            "comments": "Este es un análisis de muestra. En un sistema real, aquí se evaluaría si la respuesta cubre todos los aspectos importantes de la pregunta."
        },
        "precision_tecnica": {
            "score": 0,
            "comments": "Este es un análisis de muestra. En un sistema real, aquí se evaluaría si hay errores conceptuales o técnicos."
        },
        "estructura_claridad": {
            "score": 0,
            "comments": "Este es un análisis de muestra. En un sistema real, aquí se evaluaría la estructura y claridad de la respuesta."
        },
        "fuentes": {
            "score": 0,
            "comments": "Este es un análisis de muestra. En un sistema real, aquí se evaluaría si la respuesta cita fuentes o se basa en conocimiento general plausible."
        },
        "limitaciones_desafios": {
            "score": 0,
            "comments": "Este es un análisis de muestra. En un sistema real, aquí se evaluaría si la respuesta identifica limitaciones, desafíos o trade-offs."
        },
        "sesgos": {
            "score": 0,
            "comments": "Este es un análisis de muestra. En un sistema real, aquí se evaluaría si la respuesta presenta sesgos obvios."
        },
        "profundidad": {
            "score": 0,
            "comments": "Este es un análisis de muestra. En un sistema real, aquí se evaluaría la profundidad de la respuesta."
        }
    }
    
    # Calcular puntuación total
    total_score = sum(item["score"] for item in analysis.values()) / len(analysis)
    
    # Generar recomendaciones para mejorar
    recommendations = "Este es un análisis de muestra. En un sistema real, aquí se generarían recomendaciones específicas para mejorar la respuesta basadas en los criterios anteriores."
    
    # Mejorar la respuesta
    improved_response = "Este es un análisis de muestra. En un sistema real, aquí se generaría una versión mejorada de la respuesta original."
    
    return {
        "question_key": question_key,
        "analysis": analysis,
        "total_score": total_score,
        "recommendations": recommendations,
        "improved_response": improved_response
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
            
            f.write(f"\n**Puntuación total**: {analysis_data['total_score']}/10\n\n")
            
            f.write("### Recomendaciones para mejorar\n\n")
            f.write(f"{analysis_data['recommendations']}\n\n")
            
            f.write("### Respuesta mejorada\n\n")
            f.write(f"{analysis_data['improved_response']}\n\n")
            
            f.write("### Reflexión sobre el proceso\n\n")
            f.write("En esta sección, se debería reflexionar sobre:\n")
            f.write("- ¿Qué tan útil fue la IA en esta respuesta?\n")
            f.write("- ¿Dónde falló?\n")
            f.write("- ¿Qué tipo de aspectos de la pregunta manejó mejor/peor?\n\n")
            
            f.write("---\n\n")

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Analiza críticamente las respuestas del sistema multi-agente")
    parser.add_argument(
        "--input", 
        type=str, 
        default="./outputs/resumen_respuestas.txt",
        help="Archivo de entrada con las respuestas a analizar"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default="./outputs/analisis_critico.md",
        help="Archivo de salida con el análisis crítico"
    )
    parser.add_argument(
        "--question", 
        type=str, 
        default=None,
        help="Clave específica de pregunta a analizar (por defecto, todas)"
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
        analyses[question_key] = analyze_response(question_key, response_data)
    
    # Generar informe
    generate_report(analyses, args.output)
    logger.info(f"Informe generado: {args.output}")

if __name__ == "__main__":
    main() 