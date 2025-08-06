# src/storage/__init__.py
"""Storage module initialization."""
from pathlib import Path
import sys
from typing import Dict, Any
from .wallet_manager import WalletManager
from .database import Database

__all__ = ['WalletManager', 'Database']

def setup_storage(config: Dict[str, Any]) -> Dict[str, Any]:
    """Initialize storage components."""
    wallet_manager = WalletManager(config.get('wallet', {}))
    database = Database(config.get('database', {}))
    return {'wallet': wallet_manager, 'database': database}
