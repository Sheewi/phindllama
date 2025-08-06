# src/storage/wallet_storage.py
"""Wallet storage implementation."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging
from datetime import datetime
from ..config.settings import Settings

class WalletStorage(ABC):
    """
    Base wallet storage class.
    
    Handles persistent storage of wallet-related data.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.settings = Settings().get_default_settings()['wallet_storage']
        
    @abstractmethod
    def store_transaction(self, tx_data: Dict[str, Any]) -> bool:
        """Store transaction data."""
        pass
        
    def validate_transaction(self, tx_data: Dict[str, Any]) -> bool:
        """Validate transaction data before storage."""
        required_fields = ['tx_id', 'timestamp', 'amount', 'currency']
        return all(field in tx_data for field in required_fields)
        
    def get_transaction_history(self, 
                              start_date: Optional[datetime] = None,
                              end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Retrieve transaction history within date range."""
        if start_date and end_date:
            return self._filter_by_date_range(start_date, end_date)
        return self._get_all_transactions()
