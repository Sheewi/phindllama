# src/agents/trading_agent.py
from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

class TradingAgent(ABC):
    def __init__(self, wallet_interface, market_data_feed):
        self.logger = logging.getLogger(__name__)
        self.wallet = wallet_interface
        self.market_data = market_data_feed
        self.fuzzy_logic_engine = FuzzyLogicEngine()
        
    @abstractmethod
    def execute_trade(self, strategy: Dict) -> bool:
        """Execute a trading operation based on strategy"""
        pass
        
    def update_strategy(self, new_strategy: Dict) -> None:
        """Update trading strategy parameters"""
        self.validate_strategy(new_strategy)
        self.strategy = new_strategy
        self.logger.info(f"Updated trading strategy: {new_strategy}")
