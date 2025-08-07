# src/core/mcp_controller.py
from typing import Dict, List
import logging
from .agent_factory import AgentFactory

class MCPController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.agent_factory = AgentFactory()
        self.active_agents: Dict[str, object] = {}
        self.initialized = False
        
    def initialize(self, config: dict) -> bool:
        """Initialize the controller with configuration"""
        try:
            self._setup_logging()
            self._load_config(config)
            self.initialized = True
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize MCP controller: {e}")
            return False
        
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
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(level=logging.INFO)
        
    def _load_config(self, config: dict):
        """Load configuration settings"""
        self.config = config
