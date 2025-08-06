# src/core/__init__.py
"""Core module initialization."""
from pathlib import Path
import sys
from typing import Dict, Any
from .mcp_controller import MCPController
from .agent_factory import AgentFactory

def setup_core():
    """Initialize core components."""
    return {
        'controller': MCPController(),
        'factory': AgentFactory()
    }

__all__ = ['setup_core', 'MCPController', 'AgentFactory']
