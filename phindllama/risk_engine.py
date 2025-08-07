# phindllama/risk_engine.py
"""Risk management engine for monitoring and controlling system operations."""
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class RiskEngine:
    """Risk management and monitoring engine."""
    
    def __init__(self, thresholds: Optional[Dict[str, Any]] = None):
        self.thresholds = thresholds or self._get_default_thresholds()
        self.violations = []
        self.metrics = {}
        self.monitoring_active = False
        self._initialize_monitoring()
    
    def _get_default_thresholds(self) -> Dict[str, Any]:
        """Get default risk thresholds."""
        return {
            'daily_volume': 5.0,  # ETH
            'tx_frequency': 30,   # per hour
            'slippage': 0.05,     # 5%
            'max_position_size': 1000.0,  # USD
            'loss_limit': 0.10,   # 10% loss limit
            'gas_price_limit': 100,  # gwei
            'api_call_rate': 1000,  # per minute
            'memory_usage': 0.8,  # 80% of available
            'cpu_usage': 0.9      # 90% of available
        }
    
    def _initialize_monitoring(self):
        """Initialize risk monitoring systems."""
        self.risk_categories = {
            'financial': ['daily_volume', 'max_position_size', 'loss_limit'],
            'operational': ['tx_frequency', 'gas_price_limit', 'api_call_rate'],
            'technical': ['memory_usage', 'cpu_usage'],
            'market': ['slippage']
        }
        
        logger.info("Risk engine initialized with thresholds: %s", self.thresholds)
    
    @contextmanager
    def monitor(self):
        """Context manager for risk monitoring during operations."""
        self.monitoring_active = True
        start_time = datetime.now()
        
        try:
            logger.info("Risk monitoring started")
            yield self
        except Exception as e:
            self._handle_risk_violation('operation_failure', {'error': str(e)})
            raise
        finally:
            self.monitoring_active = False
            duration = datetime.now() - start_time
            logger.info(f"Risk monitoring ended after {duration.total_seconds():.2f}s")
    
    def check_risk(self, category: str, metric: str, value: float) -> bool:
        """Check if a metric violates risk thresholds."""
        threshold = self.thresholds.get(metric)
        
        if threshold is None:
            logger.warning(f"No threshold defined for metric: {metric}")
            return True
        
        # Record the metric
        self.metrics[metric] = {
            'value': value,
            'threshold': threshold,
            'timestamp': datetime.now(),
            'category': category
        }
        
        # Check for violation
        violation = value > threshold
        
        if violation:
            self._handle_risk_violation(metric, {
                'value': value,
                'threshold': threshold,
                'category': category
            })
        
        return not violation
    
    def _handle_risk_violation(self, metric: str, details: Dict[str, Any]):
        """Handle a risk threshold violation."""
        violation = {
            'metric': metric,
            'details': details,
            'timestamp': datetime.now(),
            'severity': self._assess_severity(metric, details)
        }
        
        self.violations.append(violation)
        
        # Log based on severity
        severity = violation['severity']
        if severity == 'critical':
            logger.critical(f"CRITICAL risk violation: {metric} = {details}")
        elif severity == 'high':
            logger.error(f"HIGH risk violation: {metric} = {details}")
        elif severity == 'medium':
            logger.warning(f"MEDIUM risk violation: {metric} = {details}")
        else:
            logger.info(f"LOW risk violation: {metric} = {details}")
        
        # Take automated action if needed
        self._take_automated_action(violation)
    
    def _assess_severity(self, metric: str, details: Dict[str, Any]) -> str:
        """Assess the severity of a risk violation."""
        value = details.get('value', 0)
        threshold = details.get('threshold', 0)
        
        if threshold == 0:
            return 'low'
        
        ratio = value / threshold
        
        if ratio >= 2.0:
            return 'critical'
        elif ratio >= 1.5:
            return 'high'
        elif ratio >= 1.2:
            return 'medium'
        else:
            return 'low'
    
    def _take_automated_action(self, violation: Dict[str, Any]):
        """Take automated action based on risk violation."""
        metric = violation['metric']
        severity = violation['severity']
        
        if severity in ['critical', 'high']:
            if metric in ['daily_volume', 'max_position_size']:
                logger.warning(f"Triggering position size reduction due to {metric}")
                self._reduce_position_sizes()
            elif metric == 'loss_limit':
                logger.warning("Triggering emergency stop due to loss limit")
                self._emergency_stop()
            elif metric in ['memory_usage', 'cpu_usage']:
                logger.warning(f"Triggering resource optimization due to {metric}")
                self._optimize_resources()
    
    def _reduce_position_sizes(self):
        """Reduce position sizes to manage risk."""
        logger.info("Implementing position size reduction")
        # Simulate position reduction
        reduction_factor = 0.5
        logger.info(f"Position sizes reduced by {(1-reduction_factor)*100}%")
    
    def _emergency_stop(self):
        """Emergency stop all trading operations."""
        logger.critical("EMERGENCY STOP: All trading operations halted")
        # In a real system, this would stop all active trades
    
    def _optimize_resources(self):
        """Optimize system resource usage."""
        logger.info("Optimizing system resources")
        # Simulate resource optimization
    
    def get_risk_status(self) -> Dict[str, Any]:
        """Get current risk status."""
        recent_violations = [
            v for v in self.violations 
            if v['timestamp'] > datetime.now() - timedelta(hours=24)
        ]
        
        risk_score = self._calculate_risk_score()
        
        return {
            'risk_score': risk_score,
            'status': self._get_risk_status_level(risk_score),
            'monitoring_active': self.monitoring_active,
            'total_violations': len(self.violations),
            'recent_violations': len(recent_violations),
            'violations_24h': recent_violations,
            'current_metrics': self.metrics,
            'thresholds': self.thresholds,
            'last_updated': datetime.now().isoformat()
        }
    
    def _calculate_risk_score(self) -> float:
        """Calculate overall risk score (0.0 = low risk, 1.0 = high risk)."""
        if not self.violations:
            return 0.0
        
        # Weight recent violations more heavily
        now = datetime.now()
        score = 0.0
        
        for violation in self.violations:
            age_hours = (now - violation['timestamp']).total_seconds() / 3600
            age_weight = max(0.1, 1.0 - (age_hours / 24))  # Decay over 24 hours
            
            severity_weights = {
                'critical': 1.0,
                'high': 0.7,
                'medium': 0.4,
                'low': 0.1
            }
            
            severity_weight = severity_weights.get(violation['severity'], 0.1)
            score += severity_weight * age_weight
        
        return min(1.0, score / 10)  # Normalize to 0-1 range
    
    def _get_risk_status_level(self, risk_score: float) -> str:
        """Get risk status level based on score."""
        if risk_score >= 0.8:
            return 'critical'
        elif risk_score >= 0.6:
            return 'high'
        elif risk_score >= 0.4:
            return 'medium'
        elif risk_score >= 0.2:
            return 'low'
        else:
            return 'minimal'
    
    def update_thresholds(self, new_thresholds: Dict[str, Any]):
        """Update risk thresholds."""
        self.thresholds.update(new_thresholds)
        logger.info(f"Risk thresholds updated: {new_thresholds}")
    
    def clear_violations(self, older_than_hours: int = 24):
        """Clear old violations."""
        cutoff = datetime.now() - timedelta(hours=older_than_hours)
        
        old_count = len(self.violations)
        self.violations = [
            v for v in self.violations 
            if v['timestamp'] > cutoff
        ]
        new_count = len(self.violations)
        
        logger.info(f"Cleared {old_count - new_count} violations older than {older_than_hours} hours")
    
    def simulate_market_conditions(self, volatility: float = 0.1):
        """Simulate various market conditions for testing."""
        import random
        
        # Simulate some metrics with the given volatility
        simulated_metrics = {
            'daily_volume': random.uniform(0, 10) * (1 + volatility),
            'slippage': random.uniform(0, 0.15) * (1 + volatility),
            'gas_price_limit': random.uniform(20, 200) * (1 + volatility)
        }
        
        for metric, value in simulated_metrics.items():
            self.check_risk('market', metric, value)
        
        logger.info(f"Simulated market conditions with volatility {volatility}")
        
        return simulated_metrics