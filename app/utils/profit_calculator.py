# app/utils/profit_calculator.py
from typing import Dict, Any
import math
from datetime import datetime, timedelta

class ProfitCalculator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.memory = PersistentMemory(config['memory'])
        
    def calculate_profit_margin(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate profit margin for a transaction."""
        fees = self._calculate_fees(transaction_data)
        profit = transaction_data['amount'] - transaction_data['cost']
        margin = (profit / transaction_data['cost']) * 100
        
        return {
            'profit': profit,
            'margin': margin,
            'fees': fees,
            'timestamp': datetime.now(),
            'scaling_factor': self._calculate_scaling_factor(margin)
        }
        
    def _calculate_fees(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate all applicable fees."""
        return {
            'transaction': transaction_data['amount'] * self.config['transaction_fee'],
            'gas': transaction_data.get('gas_cost', 0),
            'management': transaction_data['amount'] * self.config['management_fee']
        }
        
    def _calculate_scaling_factor(self, margin: float) -> float:
        """Calculate scaling factor based on profit margin."""
        if margin > self.config['high_margin_threshold']:
            return 1.2
        elif margin < self.config['low_margin_threshold']:
            return 0.8
        return 1.0