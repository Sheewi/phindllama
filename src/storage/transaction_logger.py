# src/storage/transaction_logger.py
"""Transaction logging implementation."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging
from datetime import datetime
from ..config.settings import Settings

class TransactionLogger(ABC):
    """
    Base transaction logging class.
    
    Handles logging of all transactions and related events.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.settings = Settings().get_default_settings()['transaction_logging']
        
    @abstractmethod
    def log_transaction(self, tx_data: Dict[str, Any]) -> bool:
        """Log a transaction."""
        pass
        
    def _format_log_entry(self, tx_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format transaction data for logging."""
        return {
            'timestamp': datetime.utcnow(),
            'tx_id': tx_data['tx_id'],
            'amount': tx_data['amount'],
            'currency': tx_data['currency'],
            'status': tx_data['status'],
            'metadata': tx_data.get('metadata', {})
        }
        
    def _store_log_entry(self, log_entry: Dict[str, Any]) -> bool:
        """Store formatted log entry."""
        try:
            self._write_to_storage(log_entry)
            return True
        except Exception as e:
            self.logger.error(f"Failed to store log entry: {str(e)}")
            return False
