# src/utils/scaling_manager.py
"""Scaling operations with web traffic monitoring."""
import logging
from typing import Dict, Any, Optional
import requests
from ..config.settings import Settings

class ScalingManager:
    """
    Scaling manager with web traffic monitoring and revenue optimization.
    
    Monitors web traffic and system load to determine scaling needs.
    """
    def __init__(self, config: Dict[str, Any]):
        self.logger = logging.getLogger(__name__)
        self.config = {**Settings().get_default_settings()['scaling'], **config}
        self.web_traffic_monitor = self._initialize_web_monitor()
        
    def _initialize_web_monitor(self) -> Any:
        """Initialize web traffic monitoring."""
        try:
            from .web_interface import WebInterface
            return WebInterface(self.config.get('web', {}))
        except ImportError:
            # Mock web interface for testing
            class MockWebInterface:
                def __init__(self, config):
                    self.config = config
                    
                def get_traffic_metrics(self):
                    return {
                        'requests_per_minute': 500,
                        'response_time': 200,
                        'error_rate': 0.01
                    }
            
            return MockWebInterface(self.config.get('web', {}))
        
    def evaluate_scaling(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate scaling needs based on web traffic and revenue metrics.
        
        Args:
            metrics: System metrics including web traffic and revenue data
            
        Returns:
            Dictionary containing scaling recommendations and revenue projections
        """
        web_traffic = self.web_traffic_monitor.get_traffic_metrics()
        revenue_trend = self._analyze_revenue_trend(metrics)
        
        scaling_decision = self._determine_scaling(web_traffic, revenue_trend)
        
        return {
            'scaling_decision': scaling_decision,
            'revenue_projection': revenue_trend['projection'],
            'recommended_instances': self._calculate_instances(scaling_decision)
        }
        
    def _analyze_revenue_trend(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze revenue trends from web interactions."""
        revenue_data = metrics.get('revenue', [])
        if not revenue_data:
            return {'projection': 0, 'trend': 'stable'}
            
        # Calculate trend and project future revenue
        trend = self._calculate_trend(revenue_data)
        projection = self._project_revenue(trend, revenue_data[-1])
        
        return {'projection': projection, 'trend': trend}
    
    def _determine_scaling(self, web_traffic: Dict[str, Any], revenue_trend: Dict[str, Any]) -> str:
        """Determine scaling decision based on traffic and revenue."""
        traffic_level = web_traffic.get('requests_per_minute', 0)
        revenue_projection = revenue_trend.get('projection', 0)
        
        if traffic_level > 1000 or revenue_projection > 100:
            return 'scale_up'
        elif traffic_level < 100 and revenue_projection < 10:
            return 'scale_down'
        else:
            return 'maintain'
    
    def _calculate_instances(self, scaling_decision: str) -> int:
        """Calculate recommended number of instances."""
        base_instances = 2
        if scaling_decision == 'scale_up':
            return base_instances * 2
        elif scaling_decision == 'scale_down':
            return max(1, base_instances // 2)
        else:
            return base_instances
    
    def _calculate_trend(self, revenue_data: list) -> str:
        """Calculate revenue trend."""
        if len(revenue_data) < 2:
            return 'stable'
        
        recent = sum(revenue_data[-3:]) / min(3, len(revenue_data))
        older = sum(revenue_data[:-3]) / max(1, len(revenue_data) - 3)
        
        if recent > older * 1.1:
            return 'increasing'
        elif recent < older * 0.9:
            return 'decreasing'
        else:
            return 'stable'
    
    def _project_revenue(self, trend: str, last_value: float) -> float:
        """Project future revenue based on trend."""
        if trend == 'increasing':
            return last_value * 1.2
        elif trend == 'decreasing':
            return last_value * 0.8
        else:
            return last_value
