# src/core/mcp_controller.py
from typing import Dict, List
import logging
from .agent_factory import AgentFactory

class MCPController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.agent_factory = AgentFactory()
        self.active_agents: Dict[str, object] = {}
        
    def initialize(self, config: dict) -> None:
        """Initialize the controller with configuration"""
        self._setup_logging()
        self._load_config(config)
        
    def create_agent(self, agent_type: str, config: dict) -> str:
        """Create and deploy a new agent"""
        agent_id = self.agent_factory.create(agent_type, config)
        self.active_agents[agent_id] = self.agent_factory.get_agent(agent_id)
        return agent_id
        
    def monitor_performance(self) -> Dict:
        """Monitor and collect performance metrics"""
        metrics = {}
        for agent_id, agent in self.active_agents.items():
            metrics[agent_id] = agent.collect_metrics()
        return metrics
