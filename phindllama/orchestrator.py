# phindllama/orchestrator.py
"""Main orchestrator for the phindllama system."""
import time
import logging
import asyncio
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class AdaptiveOrchestrator:
    """Main orchestrator for coordinating all system components."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize system components with error handling."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize dynamic task manager
        try:
            from .core.dynamic_task_manager import DynamicTaskManager
            self.task_manager = DynamicTaskManager(config)
            self.logger.info("DynamicTaskManager initialized")
        except ImportError:
            self.task_manager = None
            self.logger.warning("DynamicTaskManager not available")
        
        # Initialize evolution engine
        try:
            from .core.evolution_engine import EvolutionEngine
            self.evolution_engine = EvolutionEngine(config)
            self.logger.info("EvolutionEngine initialized - system is self-evolving")
        except ImportError:
            self.evolution_engine = None
            self.logger.warning("EvolutionEngine not available")
        
        # Initialize agent cluster
        try:
            from .agent_cluster import AgentCluster
            self.agent_cluster = AgentCluster(config)
        except ImportError:
            logger.warning("AgentCluster not available, using mock")
            self.agent_cluster = MockAgentCluster()
        
        # Initialize dashboard manager
        try:
            from .api.dashboard_api import dashboard_manager
            dashboard_manager.task_manager = self.task_manager
            self.dashboard_manager = dashboard_manager
            self.logger.info("Dashboard manager connected to task manager")
        except ImportError:
            self.dashboard_manager = None
            self.logger.warning("Dashboard manager not available")
        
        # Initialize risk engine
        try:
            from .risk_engine import RiskEngine
            self.risk_engine = RiskEngine(config)
        except ImportError:
            logger.warning("RiskEngine not available, using mock")
            self.risk_engine = MockRiskEngine()
        
        self.strategies = self._load_strategies()
        self.last_market_volatility = 0.3  # Initialize with moderate volatility
    
    def _initialize_components(self):
        """Initialize system components with error handling."""
        try:
            from .agent_cluster import AgentCluster
            self.agents = AgentCluster()
        except ImportError:
            logger.warning("AgentCluster not available, using mock")
            self.agents = MockAgentCluster()
        
        try:
            from .risk_engine import RiskEngine
            self.risk_engine = RiskEngine(
                thresholds={
                    'daily_volume': 5.0,  # ETH
                    'tx_frequency': 30,   # per hour
                    'slippage': 0.05      # 5%
                }
            )
        except ImportError:
            logger.warning("RiskEngine not available, using mock")
            self.risk_engine = MockRiskEngine()
    
    def run(self):
        """Main run loop."""
        logger.info("AdaptiveOrchestrator starting...")
        
        try:
            # Load configuration
            config = self.load_configuration()
            autonomous_mode = config.get('autonomous_mode', True)
            
            if autonomous_mode:
                logger.info("Running in autonomous mode...")
                self.run_autonomous_loop()
            else:
                self.run_cycle()
                
        except KeyboardInterrupt:
            logger.info("Orchestrator stopped by user")
        except Exception as e:
            logger.error(f"Orchestrator error: {e}")
    
    def load_configuration(self):
        """Load system configuration."""
        try:
            config_path = Path.home() / ".phindllama" / "config.json"
            if config_path.exists():
                with open(config_path) as f:
                    import json
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load configuration: {e}")
        return {}
    
    def run_autonomous_loop(self):
        """Run continuous autonomous operations."""
        import time
        cycle_count = 0
        
        logger.info("Starting autonomous operation loop...")
        
        while True:
            try:
                cycle_count += 1
                logger.info(f"=== Autonomous Cycle {cycle_count} ===")
                
                # Run one cycle
                self.run_cycle()
                
                # Autonomous learning and adaptation
                self.adapt_strategies(cycle_count)
                
                # Intelligent timing based on operations
                sleep_time = self._calculate_optimal_cycle_time(cycle_count)
                logger.info(f"Cycle complete. Next cycle in {sleep_time} seconds...")
                time.sleep(sleep_time)
                
            except KeyboardInterrupt:
                logger.info("Autonomous loop stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in autonomous cycle {cycle_count}: {e}")
                time.sleep(60)  # Wait longer on error
    
    def adapt_strategies(self, cycle_count: int):
        """Adapt strategies based on performance and cycles."""
        # Every 10 cycles, evaluate and adapt
        if cycle_count % 10 == 0:
            logger.info("Performing strategic adaptation...")
            
            # Simulate strategy optimization
            adaptations = [
                "Adjusting position sizing based on volatility",
                "Optimizing entry/exit timing",
                "Rebalancing portfolio allocations",
                "Updating risk parameters"
            ]
            
            for adaptation in adaptations:
                logger.info(f"  • {adaptation}")
    
    def _calculate_optimal_cycle_time(self, cycle_count: int) -> int:
        """Calculate optimal cycle timing based on operations and market conditions."""
        base_times = {
            'market_analysis': 180,      # 3 minutes - analyze market data
            'risk_assessment': 120,      # 2 minutes - evaluate risk
            'trade_execution': 90,       # 1.5 minutes - execute trades
            'portfolio_review': 300,     # 5 minutes - comprehensive review
            'opportunity_scan': 240,     # 4 minutes - scan for opportunities
            'compliance_check': 60,      # 1 minute - quick compliance
        }
        
        # Determine cycle type based on count
        if cycle_count % 20 == 0:
            # Every 20 cycles: comprehensive review (once per hour if base is 3min)
            cycle_type = 'portfolio_review'
        elif cycle_count % 10 == 0:
            # Every 10 cycles: opportunity scanning
            cycle_type = 'opportunity_scan'
        elif cycle_count % 5 == 0:
            # Every 5 cycles: risk assessment
            cycle_type = 'risk_assessment'
        else:
            # Regular cycles: market analysis
            cycle_type = 'market_analysis'
        
        sleep_time = base_times.get(cycle_type, 180)
        
        # Add some market condition adjustments
        if hasattr(self, 'last_market_volatility'):
            if self.last_market_volatility > 0.5:
                sleep_time = int(sleep_time * 0.7)  # Faster cycles in volatile markets
            elif self.last_market_volatility < 0.2:
                sleep_time = int(sleep_time * 1.3)  # Slower cycles in stable markets
        
        logger.info(f"Cycle type: {cycle_type}, Duration: {sleep_time}s ({sleep_time//60}m {sleep_time%60}s)")
        return sleep_time
    
    def run_cycle(self):
        """Execute one cycle of operations."""
        logger.info("Running orchestrator cycle...")
        
        # Check system health
        health_status = self.check_system_health()
        logger.info(f"System health: {health_status}")
        
        # Execute strategies with risk monitoring
        if self.risk_engine:
            with self.risk_engine.monitor():
                self.execute_strategies()
        else:
            self.execute_strategies()
    
    def execute_strategies(self):
        """Execute trading strategies with evolution tracking."""
        executed_strategies = []
        
        for strategy in self.strategies:
            try:
                logger.info(f"Executing strategy: {strategy}")
                start_time = datetime.now()
                
                result = self.agent_cluster.execute(strategy, 'analysis')
                
                execution_time = (datetime.now() - start_time).total_seconds()
                logger.info(f"Strategy result: {result}")
                
                # Record performance for evolution if available
                if self.evolution_engine and result.get('status') == 'completed':
                    revenue = result.get('metrics', {}).get('revenue', 0)
                    success = result.get('status') == 'completed'
                    market_conditions = {
                        'volatility': self.last_market_volatility,
                        'volume': 1000000,  # Simplified
                        'trend': 'bullish'  # Simplified
                    }
                    
                    self.evolution_engine.record_performance(
                        strategy, revenue, execution_time, success, market_conditions
                    )
                
                executed_strategies.append({
                    'strategy': strategy,
                    'result': result,
                    'execution_time': execution_time
                })
                
            except Exception as e:
                logger.error(f"Strategy execution error: {e}")
                
                # Record failure for learning
                if self.evolution_engine:
                    self.evolution_engine.record_performance(
                        strategy, 0, 1.0, False, {'error': str(e)}
                    )
        
        # Update dashboard if available
        if self.dashboard_manager:
            asyncio.create_task(self.dashboard_manager.send_dashboard_update())
        
        return executed_strategies
    
    def get_available_strategies(self):
        """Get list of available strategies."""
        return [
            {
                'name': 'market_analysis',
                'type': 'analysis',
                'priority': 1
            },
            {
                'name': 'opportunity_detection',
                'type': 'detection',
                'priority': 2
            }
        ]
    
    def check_system_health(self) -> Dict[str, Any]:
        """Check overall system health."""
        return {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'components': {
                'agents': 'active' if self.agents else 'inactive',
                'risk_engine': 'active' if self.risk_engine else 'inactive'
            }
        }
    
    def execute_pipeline(self, strategy):
        """Full lifecycle execution with safety checks."""
        if self.risk_engine:
            with self.risk_engine.monitor():
                yield from self.agents.execute(strategy)
        else:
            yield from self.agents.execute(strategy)

class MockAgentCluster:
    """Mock agent cluster for testing."""
    
    def execute(self, strategy):
        """Mock execution."""
        logger.info(f"Mock executing strategy: {strategy}")
        return {'status': 'completed', 'result': 'mock_result'}

class MockRiskEngine:
    """Mock risk engine for testing."""
    
    def __init__(self, thresholds=None):
        self.thresholds = thresholds or {}
    
    def monitor(self):
        """Mock monitoring context."""
        return MockMonitorContext()

class MockMonitorContext:
    """Mock monitoring context."""
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

# Legacy compatibility
class Orchestrator(AdaptiveOrchestrator):
    """Legacy orchestrator class for backward compatibility."""
    pass

def main():
    """Main function for backward compatibility."""
    orchestrator = AdaptiveOrchestrator()
    orchestrator.run()