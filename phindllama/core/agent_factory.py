# src/core/agent_factory.py
"""Agent creation and management factory."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Type
import logging
from ..config.settings import Settings

class AgentFactory:
    """
    Factory pattern implementation for creating agents.
    
    Handles agent lifecycle management and configuration.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.agent_types: Dict[str, Type] = {}
        self.settings = Settings().get_default_settings()
        
    def register_agent_type(self, agent_type: str, agent_class: Type) -> None:
        """Register a new agent type."""
        self.agent_types[agent_type] = agent_class
        
    def create(self, agent_type: str, config: Dict[str, Any]) -> str:
        """Create a new agent instance."""
        if agent_type not in self.agent_types:
            raise ValueError(f"Unknown agent type: {agent_type}")
            
        agent_id = f"{agent_type}_{len(self.active_agents):04d}"
        agent = self.agent_types[agent_type](config)
        self._initialize_agent(agent, agent_id)
        return agent_id
        
    def _initialize_agent(self, agent: Any, agent_id: str) -> None:
        """Initialize agent with basic configuration."""
        agent.id = agent_id
        agent.logger = logging.getLogger(f"{__name__}.{agent_id}")
