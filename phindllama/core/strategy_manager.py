"""
Utility to set up additional trading strategies
"""
import logging
from enum import Enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import datetime
import uuid

logger = logging.getLogger(__name__)

class StrategyType(Enum):
    ARBITRAGE = "arbitrage"
    TREND_FOLLOWING = "trend_following"
    GRID_TRADING = "grid_trading"
    MEAN_REVERSION = "mean_reversion"
    STATISTICAL_ARBITRAGE = "statistical_arbitrage"
    MOMENTUM = "momentum"
    SENTIMENT_ANALYSIS = "sentiment_analysis"

@dataclass
class TradingStrategy:
    id: str
    name: str
    type: StrategyType
    description: str
    parameters: Dict[str, Any]
    performance_metrics: Dict[str, float]
    is_active: bool
    created_at: datetime.datetime
    last_updated: datetime.datetime
    risk_level: int  # 1-5, with 5 being highest risk
    
    @property
    def risk_level_text(self) -> str:
        risk_map = {
            1: "Very Low",
            2: "Low",
            3: "Moderate",
            4: "High",
            5: "Very High"
        }
        return risk_map.get(self.risk_level, "Unknown")

class StrategyManager:
    """Manages trading strategies"""
    
    def __init__(self):
        self.strategies: Dict[str, TradingStrategy] = {}
        self.initialize_default_strategies()
        
    def initialize_default_strategies(self):
        """Create default trading strategies."""
        now = datetime.datetime.now()
        
        # Arbitrage strategy
        arbitrage = TradingStrategy(
            id=str(uuid.uuid4()),
            name="Cross-Exchange Arbitrage",
            type=StrategyType.ARBITRAGE,
            description="Exploits price differences between exchanges by buying low on one exchange and selling high on another",
            parameters={
                "min_price_difference": 0.01,  # 1% minimum difference
                "max_execution_time": 10,  # seconds
                "include_fees": True,
                "max_position_size": 5000  # USD
            },
            performance_metrics={
                "win_rate": 0.78,
                "average_return": 0.012,  # 1.2% per trade
                "sharpe_ratio": 2.4
            },
            is_active=True,
            created_at=now,
            last_updated=now,
            risk_level=2
        )
        
        # Trend following strategy
        trend_following = TradingStrategy(
            id=str(uuid.uuid4()),
            name="Multi-timeframe Trend Following",
            type=StrategyType.TREND_FOLLOWING,
            description="Identifies and follows market trends across multiple timeframes for higher confidence signals",
            parameters={
                "fast_ema": 12,
                "slow_ema": 26,
                "timeframes": ["1h", "4h", "1d"],
                "trend_confirmation": "3/3",  # All timeframes must align
                "max_position_size": 7500  # USD
            },
            performance_metrics={
                "win_rate": 0.65,
                "average_return": 0.025,  # 2.5% per trade
                "sharpe_ratio": 1.9
            },
            is_active=True,
            created_at=now,
            last_updated=now,
            risk_level=3
        )
        
        # Mean reversion strategy
        mean_reversion = TradingStrategy(
            id=str(uuid.uuid4()),
            name="Bollinger Band Mean Reversion",
            type=StrategyType.MEAN_REVERSION,
            description="Trades price reversions to the mean using Bollinger Bands",
            parameters={
                "lookback_period": 20,
                "standard_deviations": 2.0,
                "min_volume": 1000000,  # USD
                "max_position_size": 5000  # USD
            },
            performance_metrics={
                "win_rate": 0.72,
                "average_return": 0.018,  # 1.8% per trade
                "sharpe_ratio": 2.1
            },
            is_active=True,
            created_at=now,
            last_updated=now,
            risk_level=2
        )
        
        # Sentiment analysis strategy
        sentiment = TradingStrategy(
            id=str(uuid.uuid4()),
            name="LLM-based Sentiment Analysis",
            type=StrategyType.SENTIMENT_ANALYSIS,
            description="Uses large language models to analyze market sentiment from news and social media",
            parameters={
                "sentiment_threshold": 0.7,
                "news_sources": ["Bloomberg", "Reuters", "Twitter", "Reddit"],
                "update_frequency": 15,  # minutes
                "max_position_size": 3000  # USD
            },
            performance_metrics={
                "win_rate": 0.62,
                "average_return": 0.032,  # 3.2% per trade
                "sharpe_ratio": 1.7
            },
            is_active=True,
            created_at=now,
            last_updated=now,
            risk_level=4
        )
        
        # Add strategies to manager
        for strategy in [arbitrage, trend_following, mean_reversion, sentiment]:
            self.strategies[strategy.id] = strategy
            
    def get_strategy(self, strategy_id: str) -> Optional[TradingStrategy]:
        """Get a strategy by ID."""
        return self.strategies.get(strategy_id)
    
    def add_strategy(self, strategy: TradingStrategy) -> str:
        """Add a new trading strategy."""
        self.strategies[strategy.id] = strategy
        logger.info(f"Added new trading strategy: {strategy.name} (ID: {strategy.id})")
        return strategy.id
    
    def update_strategy(self, strategy_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing strategy."""
        if strategy_id not in self.strategies:
            return False
            
        strategy = self.strategies[strategy_id]
        
        # Update fields
        for key, value in updates.items():
            if hasattr(strategy, key) and key != 'id':  # Don't allow ID changes
                setattr(strategy, key, value)
                
        strategy.last_updated = datetime.datetime.now()
        return True
    
    def delete_strategy(self, strategy_id: str) -> bool:
        """Delete a strategy."""
        if strategy_id in self.strategies:
            del self.strategies[strategy_id]
            logger.info(f"Deleted strategy with ID: {strategy_id}")
            return True
        return False
    
    def activate_strategy(self, strategy_id: str) -> bool:
        """Activate a strategy."""
        if strategy_id in self.strategies:
            self.strategies[strategy_id].is_active = True
            self.strategies[strategy_id].last_updated = datetime.datetime.now()
            logger.info(f"Activated strategy: {self.strategies[strategy_id].name}")
            return True
        return False
    
    def deactivate_strategy(self, strategy_id: str) -> bool:
        """Deactivate a strategy."""
        if strategy_id in self.strategies:
            self.strategies[strategy_id].is_active = False
            self.strategies[strategy_id].last_updated = datetime.datetime.now()
            logger.info(f"Deactivated strategy: {self.strategies[strategy_id].name}")
            return True
        return False
    
    def get_all_strategies(self) -> List[TradingStrategy]:
        """Get all strategies."""
        return list(self.strategies.values())
    
    def get_active_strategies(self) -> List[TradingStrategy]:
        """Get only active strategies."""
        return [s for s in self.strategies.values() if s.is_active]
    
    def get_strategies_by_type(self, strategy_type: StrategyType) -> List[TradingStrategy]:
        """Get strategies of a specific type."""
        return [s for s in self.strategies.values() if s.type == strategy_type]
    
    def get_strategy_summary(self) -> Dict[str, Any]:
        """Get a summary of strategies for the dashboard."""
        active_count = len(self.get_active_strategies())
        strategy_types = {}
        for s in self.strategies.values():
            if s.type.value not in strategy_types:
                strategy_types[s.type.value] = 0
            strategy_types[s.type.value] += 1
        
        return {
            "total_strategies": len(self.strategies),
            "active_strategies": active_count,
            "strategy_types": strategy_types,
            "top_performing": self._get_top_performing_strategies(3)
        }
    
    def _get_top_performing_strategies(self, limit: int = 3) -> List[Dict[str, Any]]:
        """Get the top performing strategies."""
        strategies = sorted(
            self.strategies.values(),
            key=lambda s: s.performance_metrics.get("sharpe_ratio", 0),
            reverse=True
        )
        
        return [{
            "id": s.id,
            "name": s.name,
            "type": s.type.value,
            "win_rate": s.performance_metrics.get("win_rate", 0),
            "average_return": s.performance_metrics.get("average_return", 0),
            "sharpe_ratio": s.performance_metrics.get("sharpe_ratio", 0)
        } for s in strategies[:limit]]

# Create singleton instance
strategy_manager = StrategyManager()
