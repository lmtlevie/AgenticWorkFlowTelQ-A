#!/usr/bin/env python
"""
Main entry point for agent conversation for telecommunications questions
"""
import argparse
import logging
import os
import sys
from typing import List, Dict, Any, Optional

from model_provider import get_model, MockModel
from agent_utils import setup_agents, run_conversation

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Questions and expected critical analysis 
QUESTIONS = {
    "5g_network_slicing": {
        "question": "Explica el concepto de 'Network Slicing' en 5G. Describe cómo la IA podría gestionar de forma autónoma el ciclo de vida completo de un 'slice' de red (creación, monitorización, adaptación y terminación) para un caso de uso específico como vehículos conectados (V2X). ¿Qué parámetros del 'slice' (latencia, ancho de banda, fiabilidad) monitorizaría y ajustaría la IA y qué desafíos presenta esta automatización?",
        "analysis_criteria": "Evaluar la claridad de la explicación de Network Slicing, si la IA detalla bien el rol de la IA en cada fase del ciclo de vida, si los parámetros mencionados son los correctos para V2X, y si identifica desafíos realistas (seguridad entre slices, complejidad de la orquestación)."
    },
    "cloud_computing_telecoms": {
        "question": "Analiza cómo la adopción de arquitecturas Cloud (incluyendo Cloud Nativo y Edge Computing) por parte de los operadores de telecomunicaciones impacta la gestión y operación de la red.",
        "analysis_criteria": "Verificar si la IA diferencia bien entre VNF y CNF, si explica claramente la relación entre Cloud/Edge y la red Telco, si propone mecanismos de IA concretos para la orquestación (ej., predicción de carga, ubicación óptima de funciones), y si menciona las complejidades de gestionar un entorno híbrido (físico, virtual, cloud)."
    },
    "internet_traffic_evolution": {
        "question": "Considerando la evolución del tráfico de internet (crecimiento del video, IoT, gaming interactivo), ¿cómo pueden los operadores de red utilizar modelos de IA (ej., redes neuronales recurrentes, transformers) para realizar predicciones de tráfico a corto y largo plazo con alta granularidad (por tipo de servicio, por zona geográfica)? ¿Cómo impactarían estas predicciones en la planificación de capacidad y en la ingeniería de tráfico?",
        "analysis_criteria": "Evaluar si la IA sugiere modelos apropiados para series temporales complejas, si discute la calidad y granularidad de los datos necesarios, la precisión esperada de las predicciones, y cómo se traducirían esas predicciones en decisiones concretas de inversión y gestión de red."
    },
    "5g_qoe": {
        "question": "Más allá de la Calidad de Servicio (QoS) técnica, la Calidad de Experiencia (QoE) del usuario es crucial. ¿Cómo puede la IA, analizando datos de red (latencia, jitter, pérdida de paquetes) y potencialmente datos de aplicación (resolución de video, tiempo de carga), estimar la QoE percibida por usuarios de servicios 5G como streaming de video 4K o Cloud Gaming? ¿Podría la red usar esta estimación para ajustar parámetros dinámicamente?",
        "analysis_criteria": "Analizar si la IA propone métricas y modelos realistas para estimar QoE (que es subjetiva), la dificultad de obtener datos de aplicación (privacidad, encriptación), y la viabilidad de que la red reaccione en tiempo real basada en QoE estimada."
    },
    "edge_computing_telco": {
        "question": "El Edge Computing acerca el procesamiento a la fuente de datos. ¿Qué tipos de aplicaciones de IA en el ámbito de las telecomunicaciones se benefician más de ser ejecutadas en el Edge en lugar del Cloud centralizado? Considera ejemplos como el análisis de video para ciudades inteligentes, optimización de la RAN (Radio Access Network) en tiempo real, o baja latencia para IoT industrial.",
        "analysis_criteria": "Verificar si la IA justifica bien por qué esas aplicaciones específicas se benefician del Edge (latencia, ancho de banda, privacidad/soberanía de datos), si considera las limitaciones de recursos del Edge, y cómo se gestionaría el ciclo de vida de los modelos de IA en el Edge."
    }
}

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Agent conversation for telecommunications questions")
    parser.add_argument(
        "--model", 
        type=str, 
        default="deepseek-r1", 
        choices=["deepseek-r1", "mock", "ollama"],
        help="Model to use for conversation"
    )
    parser.add_argument(
        "--model-variant", 
        type=str, 
        default=None,
        help="Variant of the model to use (e.g., '32b')"
    )
    parser.add_argument(
        "--question", 
        type=str, 
        choices=list(QUESTIONS.keys()),
        help="Question to address"
    )
    parser.add_argument(
        "--output-dir", 
        type=str, 
        default="./outputs",
        help="Directory to save output files"
    )
    parser.add_argument(
        "--ollama-model", 
        type=str, 
        default="deepseek-coder:33b",
        help="Model name in Ollama (default: deepseek-coder:33b)"
    )
    parser.add_argument(
        "--ollama-api", 
        type=str, 
        default="http://localhost:11434",
        help="Ollama API base URL"
    )
    parser.add_argument(
        "--max-turns", 
        type=int, 
        default=2,
        help="Maximum number of conversation turns (default: 2)"
    )
    parser.add_argument(
        "--debug", 
        action="store_true",
        help="Enable debug logging"
    )
    return parser.parse_args()

def main():
    """Main function to run the agent conversation"""
    args = parse_args()
    
    if args.debug:
        logger.setLevel(logging.DEBUG)
        
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Get the selected model
    if args.model == "mock":
        model = MockModel()
        logger.info("Using mock model for testing")
    elif args.model == "ollama":
        # Import here to avoid circular imports
        from model_provider import OllamaModel
        model = OllamaModel(model_name=args.ollama_model, api_base=args.ollama_api)
        logger.info(f"Using Ollama model: {args.ollama_model}")
    else:
        model = get_model(args.model, model_variant=args.model_variant)
        logger.info(f"Using {args.model} model")
    
    # Get the selected question
    if args.question:
        question_key = args.question
        question_data = QUESTIONS[question_key]
        questions = {question_key: question_data}
    else:
        # Use all questions if none specified
        questions = QUESTIONS
    
    # Create a file for summary of all questions
    summary_file = os.path.join(args.output_dir, "resumen_respuestas.txt")
    with open(summary_file, "w", encoding="utf-8") as f_summary:
        f_summary.write("# RESUMEN DE RESPUESTAS Y ANÁLISIS\n\n")
    
    for q_key, q_data in questions.items():
        logger.info(f"Processing question: {q_key}")
        
        # Setup agents for this question
        agent_config = {
            "expert_agent": {
                "role": "Experto en Telecomunicaciones",
                "task": f"Responder a la pregunta: {q_data['question']}"
            },
            "critic_agent": {
                "role": "Crítico de Telecomunicaciones",
                "task": f"Analizar críticamente la respuesta según estos criterios: {q_data['analysis_criteria']}"
            },
            "facilitator_agent": {
                "role": "Facilitador de la Conversación",
                "task": "Moderar la conversación entre el Experto y el Crítico, asegurando que se aborden todos los aspectos importantes de la pregunta."
            }
        }
        
        agents = setup_agents(model, agent_config)
        
        # Run the conversation
        conversation_result = run_conversation(
            agents=agents,
            question=q_data["question"],
            analysis_criteria=q_data["analysis_criteria"],
            max_turns=args.max_turns if args.model != "mock" else 2  # Reduce turns for LLM to save tokens
        )
        
        # Save the full conversation
        output_file = os.path.join(args.output_dir, f"{q_key}_conversation.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"Question: {q_data['question']}\n\n")
            f.write(f"Analysis Criteria: {q_data['analysis_criteria']}\n\n")
            f.write("Conversation:\n\n")
            for turn in conversation_result["conversation"]:
                f.write(f"{turn['agent']}: {turn['message']}\n\n")
            f.write("\nFinal Analysis:\n\n")
            f.write(conversation_result["final_analysis"])
            
        logger.info(f"Saved conversation to {output_file}")
        
        # Extract expert response and critic analysis for the summary file
        expert_response = ""
        critic_analysis = ""
        
        # Find the first expert response
        for turn in conversation_result["conversation"]:
            if turn["agent"] == "Experto" and not expert_response:
                expert_response = turn["message"]
            
            if turn["agent"] == "Crítico" and not critic_analysis:
                critic_analysis = turn["message"]
        
        # Append to the summary file
        with open(summary_file, "a", encoding="utf-8") as f_summary:
            f_summary.write(f"## {q_key.upper().replace('_', ' ')}\n\n")
            f_summary.write(f"### Pregunta\n\n{q_data['question']}\n\n")
            f_summary.write(f"### Respuesta del Experto\n\n{expert_response}\n\n")
            #f_summary.write(f"### Análisis del Crítico\n\n{critic_analysis}\n\n")
            f_summary.write(f"### Análisis Final\n\n{conversation_result['final_analysis']}\n\n")
            f_summary.write("---\n\n")
    
    logger.info(f"Saved summary to {summary_file}")
    logger.info("Completed all questions")

if __name__ == "__main__":
    main() 