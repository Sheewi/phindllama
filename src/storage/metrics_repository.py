# src/storage/metrics_repository.py
"""Metrics repository implementation."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging
from datetime import datetime
from ..config.settings import Settings

class MetricsRepository(ABC):
    """
    Base metrics repository class.
    
    Handles storage and retrieval of system metrics.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.settings = Settings().get_default_settings()['metrics_storage']
        
    @abstractmethod
    def store_metric(self, metric_data: Dict[str, Any]) -> bool:
        """Store a metric value."""
        pass
        
    def _validate_metric(self, metric_data: Dict[str, Any]) -> bool:
        """Validate metric data structure."""
        required_fields = ['name', 'value', 'timestamp']
        return all(field in metric_data for field in required_fields)
        
    def get_metric_history(self, 
                          metric_name: str,
                          start_time: Optional[datetime] = None,
                          end_time: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Retrieve metric history within time range."""
        if not start_time or not end_time:
            return self._get_all_metrics(metric_name)
        return self._get_metrics_in_range(metric_name, start_time, end_time)
