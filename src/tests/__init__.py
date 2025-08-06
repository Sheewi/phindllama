# src/tests/__init__.py
"""Test module initialization."""
from pathlib import Path
import sys
from typing import Dict, Any
from .unit.test_mcp_controller import test_mcp_controller
from .unit.test_agents import test_agents
from .unit.test_processing import test_processing
from .integration.test_system_integration import test_system_integration
from .integration.test_error_handling import test_error_handling

__all__ = [
    'test_mcp_controller',
    'test_agents',
    'test_processing',
    'test_system_integration',
    'test_error_handling'
]

def run_tests() -> Dict[str, Any]:
    """Run all tests and return results."""
    results = {}
    
    # Unit tests
    results['mcp_controller'] = test_mcp_controller()
    results['agents'] = test_agents()
    results['processing'] = test_processing()
    
    # Integration tests
    results['system_integration'] = test_system_integration()
    results['error_handling'] = test_error_handling()
    
    return results
