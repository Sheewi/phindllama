# src/core/performance_monitor.py
"""Performance monitoring system."""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging
import time
from datetime import datetime, timedelta
from ..config.settings import Settings

class PerformanceMonitor(ABC):
    """
    Base performance monitoring class.
    
    Tracks system performance metrics and provides analysis capabilities.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.settings = Settings().get_default_settings()['monitoring']
        self.metrics: Dict[str, List[Dict[str, Any]]] = {}
        
    @abstractmethod
    def collect_metrics(self) -> Dict[str, Any]:
        """Collect performance metrics."""
        pass
        
    def analyze_performance(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze collected metrics."""
        analysis = {
            'timestamp': datetime.utcnow(),
            'metrics': metrics,
            'analysis': self._perform_analysis(metrics)
        }
        self._store_metrics(analysis)
        return analysis
        
    def _perform_analysis(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Perform detailed analysis of metrics."""
        return {
            'trend': self._calculate_trend(metrics),
            'anomalies': self._detect_anomalies(metrics),
            'recommendations': self._generate_recommendations(metrics)
        }
        
    def _store_metrics(self, metrics: Dict[str, Any]) -> None:
        """Store metrics for historical analysis."""
        timestamp = metrics['timestamp']
        self.metrics[timestamp] = metrics
        
        # Clean up old metrics
        if len(self.metrics) > self.settings['max_history']:
            oldest_timestamp = min(self.metrics.keys())
            del self.metrics[oldest_timestamp]
