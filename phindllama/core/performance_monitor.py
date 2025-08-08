# src/core/performance_monitor.py
"""Performance monitoring system."""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging
import time
import os
import psutil
import platform
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


class SystemPerformanceMonitor(PerformanceMonitor):
    """System performance monitoring implementation."""
    
    def __init__(self):
        super().__init__()
        self.prev_metrics = {}
        self.error_count = 0
        self.last_error = None
        
    def collect_metrics(self) -> Dict[str, Any]:
        """Collect system performance metrics."""
        try:
            # Get CPU metrics
            cpu_usage = psutil.cpu_percent(interval=0.5)
            
            # Get memory metrics
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            
            # Get disk metrics
            disk = psutil.disk_usage('/')
            disk_usage = disk.percent
            
            # Get network metrics
            net_io = psutil.net_io_counters()
            
            # Compare with previous metrics to calculate rates
            current_time = time.time()
            network_in_rate = 0
            network_out_rate = 0
            
            if self.prev_metrics:
                time_diff = current_time - self.prev_metrics.get('timestamp', current_time)
                if time_diff > 0:
                    network_in_rate = (net_io.bytes_recv - self.prev_metrics.get('net_in', 0)) / time_diff
                    network_out_rate = (net_io.bytes_sent - self.prev_metrics.get('net_out', 0)) / time_diff
            
            # Store current metrics for next calculation
            self.prev_metrics = {
                'timestamp': current_time,
                'net_in': net_io.bytes_recv,
                'net_out': net_io.bytes_sent
            }
            
            # Get process metrics
            process = psutil.Process(os.getpid())
            process_memory = process.memory_info().rss / (1024 * 1024)  # MB
            
            # Get load average (Linux/Unix only)
            load_avg = [0, 0, 0]
            if platform.system() != 'Windows':
                load_avg = os.getloadavg()
                
            metrics = {
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage,
                'disk_usage': disk_usage,
                'process_memory_mb': process_memory,
                'network_in_kbps': network_in_rate / 1024,
                'network_out_kbps': network_out_rate / 1024,
                'load_avg': load_avg,
                'error_count': self.error_count,
                'last_error': self.last_error
            }
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error collecting metrics: {str(e)}")
            self.error_count += 1
            self.last_error = str(e)
            return {
                'error': str(e),
                'error_count': self.error_count
            }
            
    def _calculate_trend(self, metrics: Dict[str, Any]) -> str:
        """Calculate the trend of the metrics."""
        # Simple trend calculation - check if recent CPU and memory usage is increasing
        if len(self.metrics) < 2:
            return 'stable'
            
        timestamps = sorted(self.metrics.keys())
        if len(timestamps) >= 2:
            latest = timestamps[-1]
            previous = timestamps[-2]
            
            latest_metrics = self.metrics[latest]['metrics']
            previous_metrics = self.metrics[previous]['metrics']
            
            cpu_trend = latest_metrics.get('cpu_usage', 0) - previous_metrics.get('cpu_usage', 0)
            memory_trend = latest_metrics.get('memory_usage', 0) - previous_metrics.get('memory_usage', 0)
            
            if cpu_trend > 5 or memory_trend > 5:
                return 'increasing'
            elif cpu_trend < -5 or memory_trend < -5:
                return 'decreasing'
                
        return 'stable'
        
    def _detect_anomalies(self, metrics: Dict[str, Any]) -> List[str]:
        """Detect anomalies in the metrics."""
        anomalies = []
        
        # Check for high CPU usage
        if metrics.get('cpu_usage', 0) > 85:
            anomalies.append('High CPU usage')
            
        # Check for high memory usage
        if metrics.get('memory_usage', 0) > 90:
            anomalies.append('High memory usage')
            
        # Check for high disk usage
        if metrics.get('disk_usage', 0) > 90:
            anomalies.append('High disk usage')
            
        # Check for network anomalies
        if metrics.get('network_in_kbps', 0) > 10000:  # 10 Mbps
            anomalies.append('High network input')
            
        if metrics.get('network_out_kbps', 0) > 10000:  # 10 Mbps
            anomalies.append('High network output')
            
        return anomalies
        
    def _generate_recommendations(self, metrics: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on metrics."""
        recommendations = []
        
        # CPU recommendations
        if metrics.get('cpu_usage', 0) > 80:
            recommendations.append('Consider scaling up CPU resources')
            
        # Memory recommendations
        if metrics.get('memory_usage', 0) > 85:
            recommendations.append('Increase memory allocation')
            
        # Disk recommendations
        if metrics.get('disk_usage', 0) > 85:
            recommendations.append('Clean up disk space or increase storage')
            
        # Error recommendations
        if metrics.get('error_count', 0) > 5:
            recommendations.append('Investigate system errors')
            
        return recommendations
        
    def log_error(self, error: str) -> None:
        """Log an error and update error metrics."""
        self.error_count += 1
        self.last_error = error
        self.logger.error(f"Performance error: {error}")

# Create singleton instance
performance_monitor = SystemPerformanceMonitor()
