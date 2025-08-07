# phindllama/utils/__init__.py
"""Utility module initialization."""
from pathlib import Path
import sys
from typing import Dict, Any

try:
    from .error_handler import ErrorHandler
except ImportError:
    ErrorHandler = None

try:
    from .scaling_manager import ScalingManager
except ImportError:
    ScalingManager = None

from .web_interface import WebInterface
from .payment_processor import PaymentProcessor

__all__ = ['ErrorHandler', 'ScalingManager', 'WebInterface', 'PaymentProcessor']

def setup_utils(config: Dict[str, Any]) -> Dict[str, Any]:
    """Initialize utility components with web capabilities."""
    components = {}
    
    if ErrorHandler:
        components['error_handler'] = ErrorHandler(config.get('error_handling', {}))
    
    if ScalingManager:
        components['scaling_manager'] = ScalingManager(config.get('scaling', {}))
    
    components['web_interface'] = WebInterface(config.get('web', {}))
    components['payment_processor'] = PaymentProcessor(config.get('payments', {}))
    
    return components

