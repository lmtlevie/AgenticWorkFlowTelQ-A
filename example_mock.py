#!/usr/bin/env python
"""
Example script to demonstrate how to use the CAMEL framework without LLMs
"""
import logging
import os
from typing import Dict, Any

from model_provider import MockModel
from agent_utils import setup_agents, run_conversation

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def run_example() -> None:
    """Run a simple example conversation using mock agents"""
    # Initialize the mock model
    model = MockModel()
    logger.info("Initialized mock model")
    
    # Define agent configuration
    agent_config = {
        "expert_agent": {
            "role": "Experto en Telecomunicaciones",
            "task": "Responder a preguntas sobre Network Slicing en 5G"
        },
        "critic_agent": {
            "role": "Crítico de Telecomunicaciones",
            "task": "Analizar respuestas sobre Network Slicing en 5G"
        },
        "facilitator_agent": {
            "role": "Facilitador de la Conversación",
            "task": "Moderar la conversación entre el Experto y el Crítico"
        }
    }
    
    # Set up agents
    agents = setup_agents(model, agent_config)
    logger.info("Set up agents")
    
    # Define the question and analysis criteria
    question = "Explica el concepto de 'Network Slicing' en 5G. Describe cómo la IA podría gestionar de forma autónoma el ciclo de vida completo de un 'slice' de red (creación, monitorización, adaptación y terminación) para un caso de uso específico como vehículos conectados (V2X). ¿Qué parámetros del 'slice' (latencia, ancho de banda, fiabilidad) monitorizaría y ajustaría la IA y qué desafíos presenta esta automatización?"
    
    analysis_criteria = "Evaluar la claridad de la explicación de Network Slicing, si la IA detalla bien el rol de la IA en cada fase del ciclo de vida, si los parámetros mencionados son los correctos para V2X, y si identifica desafíos realistas (seguridad entre slices, complejidad de la orquestación)."
    
    # Run the conversation
    conversation_result = run_conversation(
        agents=agents,
        question=question,
        analysis_criteria=analysis_criteria,
        max_turns=2  # Keep it short for the example
    )
    
    # Create outputs directory if it doesn't exist
    os.makedirs("outputs", exist_ok=True)
    
    # Save the conversation
    output_file = os.path.join("outputs", "example_conversation.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Question: {question}\n\n")
        f.write(f"Analysis Criteria: {analysis_criteria}\n\n")
        f.write("Conversation:\n\n")
        for turn in conversation_result["conversation"]:
            f.write(f"{turn['agent']}: {turn['message']}\n\n")
        f.write("\nFinal Analysis:\n\n")
        f.write(conversation_result["final_analysis"])
    
    logger.info(f"Saved example conversation to {output_file}")
    
    # Print a summary to the console
    print("\n--- EXAMPLE CONVERSATION SUMMARY ---\n")
    print(f"Generated a conversation with {len(conversation_result['conversation'])} turns")
    print(f"Saved to: {output_file}")
    print("\nFirst messages from each agent:")
    
    agent_first_messages = {}
    for turn in conversation_result["conversation"]:
        agent = turn["agent"]
        if agent not in agent_first_messages:
            agent_first_messages[agent] = turn["message"][:100] + "..." if len(turn["message"]) > 100 else turn["message"]
    
    for agent, message in agent_first_messages.items():
        print(f"\n{agent}: {message}")
    
    print("\n--- END OF SUMMARY ---\n")

if __name__ == "__main__":
    run_example() 