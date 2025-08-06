# src/monitoring/__init__.py
"""Monitoring module initialization."""
from pathlib import Path
import sys
from typing import Dict, Any
from .metrics_collector import MetricsCollector
from .alert_system import AlertSystem

__all__ = ['MetricsCollector', 'AlertSystem']

def setup_monitoring(config: Dict[str, Any]) -> Dict[str, Any]:
    """Initialize monitoring components."""
    metrics_collector = MetricsCollector(config.get('metrics', {}))
    alert_system = AlertSystem(config.get('alerts', {}))
    return {'collector': metrics_collector, 'alerter': alert_system}
