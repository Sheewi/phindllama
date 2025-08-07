# phindllama/core/dynamic_task_manager.py
"""
Dynamic task management and autonomous micro-agent creation system.
"""
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
import json
import asyncio
from .agent_factory import AgentFactory

class MicroAgent:
    """Lightweight micro-agent for specific tasks."""
    
    def __init__(self, task_id: str, task_type: str, config: Dict[str, Any]):
        self.task_id = task_id
        self.task_type = task_type
        self.config = config
        self.status = 'created'
        self.revenue_target = config.get('revenue_target', 0)
        self.actual_revenue = 0
        self.created_at = datetime.now()
        self.logger = logging.getLogger(f"MicroAgent.{task_id}")
        
    async def execute(self) -> Dict[str, Any]:
        """Execute the assigned task."""
        self.status = 'running'
        self.logger.info(f"Executing task: {self.task_type}")
        
        # Simulate task execution with revenue generation
        if self.task_type == 'arbitrage_trading':
            return await self._execute_arbitrage()
        elif self.task_type == 'yield_farming':
            return await self._execute_yield_farming()
        elif self.task_type == 'grant_writing':
            return await self._execute_grant_writing()
        elif self.task_type == 'content_creation':
            return await self._execute_content_creation()
        else:
            return await self._execute_generic_task()
    
    async def _execute_arbitrage(self) -> Dict[str, Any]:
        """Execute arbitrage trading task."""
        # Simulate arbitrage execution
        potential_profit = self.config.get('amount', 1000) * 0.02  # 2% profit
        self.actual_revenue += potential_profit
        
        return {
            'status': 'completed',
            'revenue_generated': potential_profit,
            'trades_executed': 3,
            'profit_margin': 0.02
        }
    
    async def _execute_yield_farming(self) -> Dict[str, Any]:
        """Execute yield farming task."""
        daily_yield = self.config.get('amount', 5000) * 0.001  # 0.1% daily
        self.actual_revenue += daily_yield
        
        return {
            'status': 'completed',
            'revenue_generated': daily_yield,
            'apy': 36.5,
            'pool': self.config.get('pool', 'ETH-USDC')
        }
    
    async def _execute_grant_writing(self) -> Dict[str, Any]:
        """Execute grant writing task."""
        grant_value = self.config.get('grant_amount', 50000)
        success_rate = 0.15  # 15% success rate
        expected_value = grant_value * success_rate
        
        return {
            'status': 'completed',
            'expected_revenue': expected_value,
            'grant_amount': grant_value,
            'submission_completed': True
        }
    
    async def _execute_content_creation(self) -> Dict[str, Any]:
        """Execute content creation task."""
        content_revenue = self.config.get('rate', 100) * self.config.get('hours', 4)
        self.actual_revenue += content_revenue
        
        return {
            'status': 'completed',
            'revenue_generated': content_revenue,
            'content_pieces': 3,
            'client_satisfaction': 0.9
        }
    
    async def _execute_generic_task(self) -> Dict[str, Any]:
        """Execute generic task."""
        base_revenue = self.config.get('revenue_estimate', 50)
        self.actual_revenue += base_revenue
        
        return {
            'status': 'completed',
            'revenue_generated': base_revenue,
            'task_completed': True
        }

class DynamicTaskManager:
    """Manages dynamic task creation and micro-agent deployment."""
    
    def __init__(self, config: Dict[str, Any]):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.agent_factory = AgentFactory()
        self.active_tasks: Dict[str, MicroAgent] = {}
        self.completed_tasks: List[Dict[str, Any]] = []
        self.daily_revenue_target = config.get('daily_revenue_target', 200)  # $200/day minimum
        self.current_daily_revenue = 0
        self.task_counter = 0
        
        # Revenue thresholds for scaling
        self.scaling_thresholds = {
            200: 1,    # 1 micro-agent at $200/day
            500: 3,    # 3 micro-agents at $500/day
            1000: 5,   # 5 micro-agents at $1000/day
            2000: 10,  # 10 micro-agents at $2000/day
            5000: 20   # 20 micro-agents at $5000/day
        }
        
        self.logger.info(f"DynamicTaskManager initialized with ${self.daily_revenue_target}/day target")
    
    async def process_natural_language_task(self, task_description: str, user_id: str = None) -> Dict[str, Any]:
        """Process natural language task and create appropriate micro-agents."""
        self.logger.info(f"Processing task: {task_description}")
        
        # Analyze task and determine type and parameters
        task_analysis = self._analyze_task(task_description)
        
        # Create micro-agents based on analysis
        agents_created = []
        for agent_spec in task_analysis['agents_needed']:
            agent_id = await self._create_micro_agent(agent_spec)
            agents_created.append(agent_id)
        
        # Execute tasks
        results = []
        for agent_id in agents_created:
            if agent_id in self.active_tasks:
                result = await self.active_tasks[agent_id].execute()
                results.append(result)
                self._update_revenue_tracking(result)
        
        return {
            'task_processed': True,
            'agents_created': len(agents_created),
            'agents_deployed': agents_created,
            'execution_results': results,
            'estimated_revenue': sum(r.get('revenue_generated', 0) for r in results),
            'processing_time': datetime.now().isoformat()
        }
    
    def _analyze_task(self, task_description: str) -> Dict[str, Any]:
        """Analyze natural language task and determine micro-agent requirements."""
        task_lower = task_description.lower()
        
        # Task type detection patterns
        if any(word in task_lower for word in ['arbitrage', 'trading', 'buy', 'sell', 'exchange']):
            return {
                'primary_type': 'arbitrage_trading',
                'agents_needed': [{
                    'type': 'arbitrage_trading',
                    'config': {
                        'amount': 10000,
                        'revenue_target': 200,
                        'risk_level': 'medium'
                    }
                }]
            }
        
        elif any(word in task_lower for word in ['yield', 'farm', 'stake', 'liquidity']):
            return {
                'primary_type': 'yield_farming',
                'agents_needed': [{
                    'type': 'yield_farming',
                    'config': {
                        'amount': 20000,
                        'pool': 'ETH-USDC',
                        'revenue_target': 100
                    }
                }]
            }
        
        elif any(word in task_lower for word in ['grant', 'funding', 'proposal', 'application']):
            return {
                'primary_type': 'grant_writing',
                'agents_needed': [{
                    'type': 'grant_writing',
                    'config': {
                        'grant_amount': 75000,
                        'foundation': 'Tech Innovation Fund',
                        'revenue_target': 500
                    }
                }]
            }
        
        elif any(word in task_lower for word in ['content', 'write', 'article', 'blog', 'social']):
            return {
                'primary_type': 'content_creation',
                'agents_needed': [{
                    'type': 'content_creation',
                    'config': {
                        'rate': 150,
                        'hours': 6,
                        'revenue_target': 900
                    }
                }]
            }
        
        else:
            # Generic task
            return {
                'primary_type': 'generic',
                'agents_needed': [{
                    'type': 'generic',
                    'config': {
                        'revenue_estimate': 100,
                        'complexity': 'medium'
                    }
                }]
            }
    
    async def _create_micro_agent(self, agent_spec: Dict[str, Any]) -> str:
        """Create and deploy a micro-agent."""
        self.task_counter += 1
        task_id = f"task_{self.task_counter:04d}_{agent_spec['type']}"
        
        micro_agent = MicroAgent(task_id, agent_spec['type'], agent_spec['config'])
        self.active_tasks[task_id] = micro_agent
        
        self.logger.info(f"Created micro-agent: {task_id} for {agent_spec['type']}")
        return task_id
    
    def _update_revenue_tracking(self, result: Dict[str, Any]):
        """Update revenue tracking and scaling decisions."""
        revenue = result.get('revenue_generated', 0)
        self.current_daily_revenue += revenue
        
        self.logger.info(f"Revenue update: +${revenue:.2f}, Daily total: ${self.current_daily_revenue:.2f}")
        
        # Check if we need to scale up
        if self.current_daily_revenue < self.daily_revenue_target:
            self._trigger_autonomous_scaling()
    
    def _trigger_autonomous_scaling(self):
        """Automatically scale up operations to meet revenue targets."""
        deficit = self.daily_revenue_target - self.current_daily_revenue
        self.logger.info(f"Revenue deficit: ${deficit:.2f}, triggering autonomous scaling")
        
        # Create additional revenue-generating tasks
        if deficit > 100:
            # Create high-value arbitrage task
            asyncio.create_task(self._create_micro_agent({
                'type': 'arbitrage_trading',
                'config': {
                    'amount': deficit * 50,  # 50x multiplier for capital
                    'revenue_target': deficit,
                    'urgency': 'high'
                }
            }))
    
    def get_performance_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive performance dashboard data."""
        active_count = len(self.active_tasks)
        completed_count = len(self.completed_tasks)
        
        return {
            'revenue_metrics': {
                'daily_target': self.daily_revenue_target,
                'current_daily': self.current_daily_revenue,
                'deficit': max(0, self.daily_revenue_target - self.current_daily_revenue),
                'progress_percentage': (self.current_daily_revenue / self.daily_revenue_target) * 100
            },
            'agent_metrics': {
                'active_agents': active_count,
                'completed_tasks': completed_count,
                'total_tasks': active_count + completed_count,
                'success_rate': completed_count / max(1, active_count + completed_count)
            },
            'scaling_status': {
                'current_tier': self._get_current_scaling_tier(),
                'next_threshold': self._get_next_threshold(),
                'auto_scaling_active': self.current_daily_revenue < self.daily_revenue_target
            },
            'active_tasks': [
                {
                    'id': agent.task_id,
                    'type': agent.task_type,
                    'status': agent.status,
                    'revenue_generated': agent.actual_revenue,
                    'target': agent.revenue_target
                }
                for agent in self.active_tasks.values()
            ]
        }
    
    def _get_current_scaling_tier(self) -> int:
        """Get current scaling tier based on revenue."""
        for threshold in sorted(self.scaling_thresholds.keys(), reverse=True):
            if self.current_daily_revenue >= threshold:
                return self.scaling_thresholds[threshold]
        return 1
    
    def _get_next_threshold(self) -> int:
        """Get next revenue threshold for scaling."""
        for threshold in sorted(self.scaling_thresholds.keys()):
            if self.current_daily_revenue < threshold:
                return threshold
        return max(self.scaling_thresholds.keys())
