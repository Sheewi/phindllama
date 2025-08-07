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
        self.active_agents: Dict[str, Any] = {}
        self.settings = Settings().get_default_settings()
        self.agent_counter = 0
        
    def register_agent_type(self, agent_type: str, agent_class: Type) -> None:
        """Register a new agent type."""
        self.agent_types[agent_type] = agent_class
        
    def create(self, agent_type: str, config: Dict[str, Any]) -> str:
        """Create a new agent instance."""
        # Create mock agent for testing
        agent_id = f"{agent_type}_{self.agent_counter:04d}"
        self.agent_counter += 1
        
        # Mock agent object
        mock_agent = MockAgent(agent_id, agent_type, config)
        self.active_agents[agent_id] = mock_agent
        self._initialize_agent(mock_agent, agent_id)
        return agent_id
    
    def get_agent(self, agent_id: str) -> Any:
        """Get agent by ID."""
        return self.active_agents.get(agent_id)
        
    def _initialize_agent(self, agent: Any, agent_id: str) -> None:
        """Initialize agent with basic configuration."""
        agent.id = agent_id
        agent.logger = logging.getLogger(f"{__name__}.{agent_id}")


class MockAgent:
    """Mock agent for testing purposes."""
    def __init__(self, agent_id: str, agent_type: str, config: Dict[str, Any]):
        self.id = agent_id
        self.type = agent_type
        self.config = config
        self.logger = None
        
    def collect_metrics(self) -> Dict[str, Any]:
        """Collect agent metrics."""
        return {
            'status': 'active',
            'uptime': 100,
            'requests_processed': 50,
            'errors': 0
        }
