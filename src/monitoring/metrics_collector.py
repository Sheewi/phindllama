# src/monitoring/metrics_collector.py
"""Performance tracking implementation."""
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
from ..config.settings import Settings

class MetricsCollector:
    """
    Collects and processes system metrics.
    
    Tracks performance indicators and generates reports.
    """
    def __init__(self, config: Dict[str, Any]):
        self.logger = logging.getLogger(__name__)
        self.config = {**Settings().get_default_settings()['metrics'], **config}
        self.metrics_store = {}
        
    def collect_metrics(self) -> Dict[str, Any]:
        """Collect system-wide metrics."""
        metrics = {
            'timestamp': datetime.utcnow(),
            'system_load': self._get_system_load(),
            'memory_usage': self._get_memory_usage(),
            'agent_performance': self._collect_agent_metrics()
        }
        
        self._store_metrics(metrics)
        return metrics
        
    def _collect_agent_metrics(self) -> Dict[str, Any]:
        """Collect metrics from active agents."""
        agent_metrics = {}
        for agent_id, agent in self.config.get('agents', {}).items():
            agent_metrics[agent_id] = {
                'uptime': self._get_agent_uptime(agent),
                'transactions': self._get_transaction_count(agent),
                'performance_score': self._calculate_performance_score(agent)
            }
        return agent_metrics
        
    def _store_metrics(self, metrics: Dict[str, Any]) -> None:
        """Store collected metrics."""
        self.metrics_store[metrics['timestamp']] = metrics
        self._prune_old_metrics()
