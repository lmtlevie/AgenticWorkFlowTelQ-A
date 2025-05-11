"""
Simplified utilities for managing agent conversations
"""
import logging
from typing import Dict, List, Any, Optional

from model_provider import ModelInterface

logger = logging.getLogger(__name__)

class Agent:
    """Simple agent that can generate responses based on a role and task"""
    
    def __init__(self, name: str, role: str, task: str, model: ModelInterface):
        """
        Initialize an agent
        
        Args:
            name: Name identifier for the agent
            role: The role the agent plays (e.g., "Experto en Telecomunicaciones")
            task: The task description for the agent
            model: The model interface to use for generating responses
        """
        self.name = name
        self.role = role
        self.task = task
        self.model = model
        self.system_prompt = f"You are a {role}. Your task is to {task}. Provide detailed and insightful responses."
        logger.info(f"Created agent '{name}' with role '{role}'")
    
    def respond(self, message: str) -> str:
        """
        Generate a response to the given message
        
        Args:
            message: The message to respond to
            
        Returns:
            The generated response
        """
        prompt = f"{self.system_prompt}\n\nInput: {message}\n\nResponse:"
        response = self.model.generate(prompt, role=self.role)
        return response

def setup_agents(model: ModelInterface, agent_config: Dict[str, Dict[str, str]]) -> Dict[str, Agent]:
    """
    Set up agents based on configuration
    
    Args:
        model: The model interface to use
        agent_config: Configuration for agents with roles and tasks
    
    Returns:
        Dictionary of agent name to Agent
    """
    agents = {}
    
    for agent_name, agent_spec in agent_config.items():
        role = agent_spec["role"]
        task = agent_spec["task"]
        
        # Create the agent
        agent = Agent(
            name=agent_name,
            role=role,
            task=task,
            model=model
        )
        
        agents[agent_name] = agent
    
    return agents

def run_conversation(agents: Dict[str, Agent], 
                    question: str, 
                    analysis_criteria: str,
                    max_turns: int = 5) -> Dict[str, Any]:
    """
    Run a conversation between agents
    
    Args:
        agents: Dictionary of agent name to Agent
        question: The question to address
        analysis_criteria: Criteria for analyzing responses
        max_turns: Maximum number of conversation turns
    
    Returns:
        Conversation results including messages and final analysis
    """
    # Extract agents
    expert_agent = agents["expert_agent"]
    critic_agent = agents["critic_agent"]
    facilitator_agent = agents["facilitator_agent"]
    
    # Initialize conversation
    conversation = []
    
    # Start with facilitator introducing the topic
    facilitator_prompt = f"Please introduce a conversation about the following question: {question}. Ask the expert to address it."
    facilitator_message = facilitator_agent.respond(facilitator_prompt)
    
    conversation.append({
        "agent": "Facilitador",
        "message": facilitator_message
    })
    
    logger.info("Facilitator started the conversation")
    
    # Now let the expert address the question
    expert_prompt = f"Please respond to this question: {question}"
    expert_message = expert_agent.respond(expert_prompt)
    
    conversation.append({
        "agent": "Experto",
        "message": expert_message
    })
    
    logger.info("Expert provided initial response")
    
    # Let the critic analyze the expert's response
    critic_prompt = f"Analyze the following response to the question '{question}' based on these criteria: {analysis_criteria}\n\nResponse: {expert_message}"
    critic_message = critic_agent.respond(critic_prompt)
    
    conversation.append({
        "agent": "Crítico",
        "message": critic_message
    })
    
    logger.info("Critic provided initial analysis")
    
    # Continue the conversation for remaining turns
    current_turn = 1
    
    while current_turn < max_turns:
        # Facilitator moderates the discussion
        facilitator_prompt = f"Based on the expert's response and the critic's analysis, what aspect should be explored further? Previous expert response: {expert_message}. Previous critic analysis: {critic_message}."
        facilitator_message = facilitator_agent.respond(facilitator_prompt)
        
        conversation.append({
            "agent": "Facilitador",
            "message": facilitator_message
        })
        
        # Expert responds to the facilitator's guidance
        expert_prompt = f"The facilitator has suggested: {facilitator_message}. Please provide more details on this aspect of the question: {question}"
        expert_message = expert_agent.respond(expert_prompt)
        
        conversation.append({
            "agent": "Experto",
            "message": expert_message
        })
        
        # Critic analyzes the expert's new response
        critic_prompt = f"Analyze the expert's latest response considering the initial criteria. Expert response: {expert_message}"
        critic_message = critic_agent.respond(critic_prompt)
        
        conversation.append({
            "agent": "Crítico",
            "message": critic_message
        })
        
        logger.info(f"Completed conversation turn {current_turn + 1}")
        current_turn += 1
    
    # Generate final analysis from the critic
    final_analysis_prompt = f"Please provide a comprehensive final analysis of the expert's responses to the question '{question}', based on these criteria: {analysis_criteria}. Summarize the strengths and weaknesses, and suggest improvements."
    
    final_analysis = critic_agent.respond(final_analysis_prompt)
    
    logger.info("Conversation completed, final analysis generated")
    
    return {
        "conversation": conversation,
        "final_analysis": final_analysis
    } 