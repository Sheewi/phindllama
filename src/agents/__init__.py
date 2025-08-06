# src/agents/__init__.py
"""Agents module initialization."""
from pathlib import Path
import sys
from typing import Dict, Any
from .trading_agent import TradingAgent
from .financial_agent import FinancialAgent

def register_agents(factory):
    """Register available agent types."""
    factory.register_agent_type('trading', TradingAgent)
    factory.register_agent_type('financial', FinancialAgent)

__all__ = ['register_agents']
