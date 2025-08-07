# app/utils/cost_tracker.py
from datetime import datetime, timedelta
from typing import Dict, Any
import logging

class CostTracker:
    def __init__(self):
        self.token_counts: Dict[str, float] = {}
        self.logger = logging.getLogger(__name__)
        
    def track(self, model: str, tokens: int) -> float:
        """Track and calculate costs for model usage."""
        # Current pricing as of 2025-08-07
        TOKEN_COST = 0.000002  # $0.002 per 1K tokens
        
        cost = (tokens * TOKEN_COST) / 1000  # Convert to thousands
        self.token_counts[model] = self.token_counts.get(model, 0) + cost
        
        # Log daily costs
        if datetime.now().hour == 0:  # Midnight
            self._log_daily_costs()
            
        return cost
        
    def _log_daily_costs(self) -> None:
        """Log daily cost summary."""
        total_cost = sum(self.token_counts.values())
        self.logger.info(
            f"Daily cost summary - Total: ${total_cost:.2f}, "
            f"By model: {self.token_counts}"
        )
        self.token_counts.clear()