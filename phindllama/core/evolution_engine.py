# phindllama/core/evolution_engine.py
"""
Self-evolving system that learns from performance and adapts strategies.
"""
import json
import numpy as np
from typing import Dict, Any, List, Tuple
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class PerformanceMetric:
    """Performance metric tracking."""
    timestamp: datetime
    strategy_type: str
    revenue_generated: float
    execution_time: float
    success_rate: float
    market_conditions: Dict[str, float]

class EvolutionEngine:
    """Self-evolving AI system that learns and adapts."""
    
    def __init__(self, config: Dict[str, Any]):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.performance_history: List[PerformanceMetric] = []
        self.strategy_weights = {
            'arbitrage_trading': 1.0,
            'yield_farming': 1.0,
            'grant_writing': 1.0,
            'content_creation': 1.0,
            'market_making': 1.0
        }
        self.learning_rate = config.get('learning_rate', 0.1)
        self.adaptation_threshold = config.get('adaptation_threshold', 10)  # metrics needed before adaptation
        self.genetic_algorithm_enabled = config.get('genetic_algorithm', True)
        
        # Strategy DNA - parameters that evolve
        self.strategy_dna = {
            'arbitrage_trading': {
                'risk_tolerance': 0.05,
                'position_size_multiplier': 1.0,
                'execution_speed': 0.8,
                'profit_threshold': 0.02
            },
            'yield_farming': {
                'pool_selection_criteria': 0.7,
                'yield_threshold': 0.001,
                'diversification_factor': 0.6,
                'risk_assessment_weight': 0.8
            },
            'content_creation': {
                'quality_vs_speed': 0.7,
                'topic_selection_weight': 0.8,
                'market_demand_sensitivity': 0.9,
                'pricing_optimization': 0.75
            }
        }
        
        self.mutation_rate = 0.05
        self.crossover_rate = 0.8
        
        self.logger.info("EvolutionEngine initialized with self-learning capabilities")
    
    def record_performance(self, strategy_type: str, revenue: float, execution_time: float, 
                          success: bool, market_conditions: Dict[str, float]):
        """Record performance metric for learning."""
        metric = PerformanceMetric(
            timestamp=datetime.now(),
            strategy_type=strategy_type,
            revenue_generated=revenue,
            execution_time=execution_time,
            success_rate=1.0 if success else 0.0,
            market_conditions=market_conditions
        )
        
        self.performance_history.append(metric)
        self.logger.info(f"Recorded performance: {strategy_type} -> ${revenue:.2f}")
        
        # Trigger adaptation if we have enough data
        if len(self.performance_history) >= self.adaptation_threshold:
            self._trigger_evolution()
    
    def _trigger_evolution(self):
        """Trigger evolutionary adaptation based on performance history."""
        self.logger.info("Triggering evolutionary adaptation...")
        
        # Analyze recent performance
        recent_metrics = self.performance_history[-self.adaptation_threshold:]
        strategy_performance = defaultdict(list)
        
        for metric in recent_metrics:
            strategy_performance[metric.strategy_type].append(metric)
        
        # Evolve each strategy
        for strategy_type, metrics in strategy_performance.items():
            self._evolve_strategy(strategy_type, metrics)
        
        # Update strategy weights based on performance
        self._update_strategy_weights(recent_metrics)
        
        self.logger.info("Evolution complete - system has adapted to new patterns")
    
    def _evolve_strategy(self, strategy_type: str, metrics: List[PerformanceMetric]):
        """Evolve specific strategy parameters using genetic algorithm principles."""
        if strategy_type not in self.strategy_dna:
            return
        
        # Calculate fitness (revenue per time unit)
        total_revenue = sum(m.revenue_generated for m in metrics)
        total_time = sum(m.execution_time for m in metrics)
        avg_success_rate = sum(m.success_rate for m in metrics) / len(metrics)
        
        fitness = (total_revenue / max(total_time, 1)) * avg_success_rate
        
        current_dna = self.strategy_dna[strategy_type]
        
        # If performance is good, reinforce current parameters
        if fitness > self._get_fitness_baseline(strategy_type):
            self.logger.info(f"Strategy {strategy_type} performing well, reinforcing parameters")
            # Small positive mutations to explore nearby parameter space
            for param, value in current_dna.items():
                mutation = np.random.normal(0, 0.02)  # Small random change
                current_dna[param] = np.clip(value + mutation, 0.1, 2.0)
        else:
            self.logger.info(f"Strategy {strategy_type} underperforming, exploring new parameters")
            # Larger mutations to explore different parameter space
            for param, value in current_dna.items():
                if np.random.random() < self.mutation_rate:
                    mutation = np.random.normal(0, 0.1)  # Larger random change
                    current_dna[param] = np.clip(value + mutation, 0.1, 2.0)
        
        # Crossover with successful strategies (if genetic algorithm enabled)
        if self.genetic_algorithm_enabled and len(strategy_performance) > 1:
            self._perform_crossover(strategy_type)
        
        self.strategy_dna[strategy_type] = current_dna
        self.logger.info(f"Evolved {strategy_type} DNA: {current_dna}")
    
    def _perform_crossover(self, strategy_type: str):
        """Perform genetic crossover with successful strategies."""
        # Find the most successful strategy type
        best_strategy = max(self.strategy_weights.items(), key=lambda x: x[1])
        
        if best_strategy[0] != strategy_type and np.random.random() < self.crossover_rate:
            # Crossover parameters
            current_dna = self.strategy_dna[strategy_type]
            best_dna = self.strategy_dna.get(best_strategy[0], {})
            
            for param in current_dna.keys():
                if param in best_dna and np.random.random() < 0.5:
                    # Take parameter from best strategy
                    current_dna[param] = (current_dna[param] + best_dna[param]) / 2
    
    def _update_strategy_weights(self, metrics: List[PerformanceMetric]):
        """Update strategy weights based on recent performance."""
        strategy_revenues = defaultdict(float)
        strategy_counts = defaultdict(int)
        
        for metric in metrics:
            strategy_revenues[metric.strategy_type] += metric.revenue_generated
            strategy_counts[metric.strategy_type] += 1
        
        # Calculate average revenue per strategy
        for strategy_type in self.strategy_weights.keys():
            if strategy_counts[strategy_type] > 0:
                avg_revenue = strategy_revenues[strategy_type] / strategy_counts[strategy_type]
                
                # Update weight using exponential moving average
                current_weight = self.strategy_weights[strategy_type]
                new_weight = current_weight * (1 - self.learning_rate) + (avg_revenue / 100) * self.learning_rate
                self.strategy_weights[strategy_type] = max(0.1, min(3.0, new_weight))
        
        self.logger.info(f"Updated strategy weights: {self.strategy_weights}")
    
    def _get_fitness_baseline(self, strategy_type: str) -> float:
        """Get fitness baseline for strategy comparison."""
        baselines = {
            'arbitrage_trading': 20.0,  # $20/hour baseline
            'yield_farming': 5.0,       # $5/hour baseline
            'grant_writing': 50.0,      # $50/hour baseline
            'content_creation': 30.0,   # $30/hour baseline
            'market_making': 15.0       # $15/hour baseline
        }
        return baselines.get(strategy_type, 10.0)
    
    def get_optimized_parameters(self, strategy_type: str) -> Dict[str, float]:
        """Get evolved parameters for a strategy."""
        return self.strategy_dna.get(strategy_type, {})
    
    def get_strategy_recommendation(self) -> str:
        """Get recommended strategy based on current weights and market conditions."""
        # Consider current market conditions (simplified)
        market_volatility = np.random.uniform(0.1, 0.8)  # In real system, get from market data
        
        adjusted_weights = {}
        for strategy, weight in self.strategy_weights.items():
            # Adjust weights based on market conditions
            if strategy == 'arbitrage_trading' and market_volatility > 0.5:
                adjusted_weights[strategy] = weight * 1.5  # Favor arbitrage in volatile markets
            elif strategy == 'yield_farming' and market_volatility < 0.3:
                adjusted_weights[strategy] = weight * 1.3  # Favor yield farming in stable markets
            else:
                adjusted_weights[strategy] = weight
        
        # Return strategy with highest adjusted weight
        recommended_strategy = max(adjusted_weights.items(), key=lambda x: x[1])[0]
        self.logger.info(f"Recommended strategy: {recommended_strategy} (weight: {adjusted_weights[recommended_strategy]:.2f})")
        
        return recommended_strategy
    
    def get_evolution_summary(self) -> Dict[str, Any]:
        """Get comprehensive evolution system summary."""
        return {
            'total_learning_cycles': len(self.performance_history) // self.adaptation_threshold,
            'strategy_weights': self.strategy_weights,
            'current_dna': self.strategy_dna,
            'performance_metrics': {
                'total_samples': len(self.performance_history),
                'avg_revenue_per_hour': sum(m.revenue_generated for m in self.performance_history) / 
                                       max(sum(m.execution_time for m in self.performance_history) / 3600, 1),
                'overall_success_rate': sum(m.success_rate for m in self.performance_history) / 
                                       max(len(self.performance_history), 1)
            },
            'genetic_parameters': {
                'mutation_rate': self.mutation_rate,
                'crossover_rate': self.crossover_rate,
                'learning_rate': self.learning_rate
            },
            'recommended_strategy': self.get_strategy_recommendation(),
            'last_evolution': self.performance_history[-1].timestamp.isoformat() if self.performance_history else None
        }
    
    def export_learned_parameters(self) -> str:
        """Export learned parameters for backup/analysis."""
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'strategy_weights': self.strategy_weights,
            'strategy_dna': self.strategy_dna,
            'performance_history_summary': {
                'total_metrics': len(self.performance_history),
                'total_revenue': sum(m.revenue_generated for m in self.performance_history),
                'avg_success_rate': sum(m.success_rate for m in self.performance_history) / max(len(self.performance_history), 1)
            }
        }
        return json.dumps(export_data, indent=2)
    
    def import_learned_parameters(self, data: str):
        """Import previously learned parameters."""
        try:
            import_data = json.loads(data)
            self.strategy_weights.update(import_data.get('strategy_weights', {}))
            self.strategy_dna.update(import_data.get('strategy_dna', {}))
            self.logger.info("Successfully imported learned parameters")
        except Exception as e:
            self.logger.error(f"Failed to import parameters: {e}")
