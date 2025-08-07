# src/utils/__init__.py
"""Utility module initialization."""
from pathlib import Path
import sys
from typing import Dict, Any
from .error_handler import ErrorHandler
from .scaling_manager import ScalingManager
from .web_interface import WebInterface
from .payment_processor import PaymentProcessor

__all__ = ['ErrorHandler', 'ScalingManager', 'WebInterface', 'PaymentProcessor']

def setup_utils(config: Dict[str, Any]) -> Dict[str, Any]:
    """Initialize utility components with web capabilities."""
    error_handler = ErrorHandler(config.get('error_handling', {}))
    scaling_manager = ScalingManager(config.get('scaling', {}))
    web_interface = WebInterface(config.get('web', {}))
    payment_processor = PaymentProcessor(config.get('payments', {}))
    
    return {
        'error_handler': error_handler,
        'scaling_manager': scaling_manager,
        'web_interface': web_interface,
        'payment_processor': payment_processor
    }

