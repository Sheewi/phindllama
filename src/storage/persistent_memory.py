# app/storage/persistent_memory.py
from typing import Dict, Any, Optional
import redis
import json
from datetime import datetime, timedelta

class PersistentMemory:
    def __init__(self, config: Dict[str, Any]):
        self.redis_client = redis.Redis(
            host=config['host'],
            port=config['port'],
            db=config['db'],
            decode_responses=True
        )
        self._initialize_memory_spaces()
        
    def _initialize_memory_spaces(self) -> None:
        """Initialize memory spaces for different data types."""
        self.memory_spaces = {
            'transactions': 'transactions:',
            'metrics': 'metrics:',
            'grants': 'grants:',
            'marketing': 'marketing:',
            'savings': 'savings:'
        }
        
    def store_transaction(self, tx_data: Dict[str, Any]) -> bool:
        """Store transaction data with TTL."""
        key = f"{self.memory_spaces['transactions']}{tx_data['tx_id']}"
        self.redis_client.hmset(key, tx_data)
        self.redis_client.expire(key, 86400)  # 24 hour TTL
        return True
        
    def get_transaction_history(self, 
                              start_date: Optional[datetime] = None,
                              end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Retrieve transaction history within date range."""
        if start_date and end_date:
            return self._filter_by_date_range(start_date, end_date)
        return self._get_all_transactions()