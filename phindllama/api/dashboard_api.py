# phindllama/api/dashboard_api.py
"""
Real-time dashboard API with wallet management, projections, and chat interface.
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json
import asyncio
from typing import Dict, Any, List
import logging
from datetime import datetime, timedelta
from ..core.dynamic_task_manager import DynamicTaskManager
from ..core.profit_monitor import profit_monitor
import os

class DashboardManager:
    """Manages real-time dashboard data and WebSocket connections."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.active_connections: List[WebSocket] = []
        self.task_manager = None
        self.profit_monitor = profit_monitor
        self.wallet_data = {
            'total_balance': 45000.00,
            'daily_pnl': 0.00,
            'positions': [],
            'transactions': []
        }
        self.system_metrics = {
            'uptime': datetime.now(),
            'total_revenue': 0.00,
            'active_strategies': 0,
            'success_rate': 0.95
        }
        
        # Initialize with some sample income for testing
        if os.environ.get('ENVIRONMENT') == 'development':
            self._init_sample_data()
    
    async def connect(self, websocket: WebSocket):
        """Connect a new WebSocket client."""
        await websocket.accept()
        self.active_connections.append(websocket)
        self.logger.info(f"Dashboard client connected. Total: {len(self.active_connections)}")
        
        # Send initial data
        await self.send_dashboard_update(websocket)
    
    def disconnect(self, websocket: WebSocket):
        """Disconnect a WebSocket client."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        self.logger.info(f"Dashboard client disconnected. Total: {len(self.active_connections)}")
    
    async def send_dashboard_update(self, websocket: WebSocket = None):
        """Send dashboard update to clients."""
        dashboard_data = await self.get_dashboard_data()
        message = json.dumps(dashboard_data)
        
        if websocket:
            # Send to specific client
            try:
                await websocket.send_text(message)
            except:
                self.disconnect(websocket)
        else:
            # Broadcast to all clients
            disconnected = []
            for connection in self.active_connections:
                try:
                    await connection.send_text(message)
                except:
                    disconnected.append(connection)
            
            # Remove disconnected clients
            for connection in disconnected:
                self.disconnect(connection)
    
    def _init_sample_data(self):
        """Initialize sample income data for development."""
        # Track some sample income for testing
        self.profit_monitor.track_income(45.75, "trading", {"pair": "ETH/USDT", "strategy": "arbitrage"})
        self.profit_monitor.track_income(23.50, "fees", {"service": "analysis", "client": "external"})
        self.profit_monitor.track_income(87.25, "trading", {"pair": "BTC/USDT", "strategy": "swing"})
        self.profit_monitor.track_expense(12.80, "infrastructure", {"service": "cloud_run", "provider": "gcp"})
        self.profit_monitor.track_expense(5.25, "fees", {"type": "transaction", "network": "ethereum"})
    
    async def get_dashboard_data(self) -> Dict[str, Any]:
        """Compile comprehensive dashboard data."""
        # Get task manager performance if available
        task_performance = {}
        if self.task_manager:
            task_performance = self.task_manager.get_performance_dashboard()
            
        # Get profit monitoring data
        profit_data = self.profit_monitor.get_dashboard_data()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'wallet': {
                'total_balance': self.wallet_data['total_balance'],
                'available_balance': self.wallet_data['total_balance'] * 0.6,
                'locked_balance': self.wallet_data['total_balance'] * 0.4,
                'daily_pnl': self.wallet_data['daily_pnl'],
                'weekly_pnl': self.wallet_data['daily_pnl'] * 7,
                'positions': len(self.wallet_data['positions']),
                'last_transaction': datetime.now().isoformat()
            },
            'revenue': {
                'daily_target': task_performance.get('revenue_metrics', {}).get('daily_target', 200),
                'daily_actual': profit_data.get('daily_income', 0),
                'progress_percent': profit_data.get('target_achievement', 0),
                'weekly_projection': profit_data.get('monthly_projection', 0) / 4,  # Monthly / 4 weeks
                'monthly_projection': profit_data.get('monthly_projection', 0)
            },
            'profit': {
                'daily': profit_data.get('daily_profit', 0),
                'total': profit_data.get('total_profit', 0),
                'roi_daily': profit_data.get('daily_roi', 0),
                'roi_total': profit_data.get('total_roi', 0),
                'annual_projection': profit_data.get('annual_projection', 0),
                'top_sources': profit_data.get('top_income_sources', [])
            },
            'agents': {
                'active_count': task_performance.get('agent_metrics', {}).get('active_agents', 0),
                'completed_tasks': task_performance.get('agent_metrics', {}).get('completed_tasks', 0),
                'success_rate': task_performance.get('agent_metrics', {}).get('success_rate', 0),
                'active_tasks': task_performance.get('active_tasks', [])
            },
            'system': {
                'status': 'operational',
                'uptime_hours': (datetime.now() - self.system_metrics['uptime']).total_seconds() / 3600,
                'cpu_usage': 35.2,
                'memory_usage': 68.5,
                'network_status': 'connected',
                'last_error': None
            },
            'market': {
                'btc_price': 65420.50,
                'eth_price': 3285.75,
                'market_volatility': 0.15,
                'trending_pairs': ['BTC/USD', 'ETH/USD', 'SOL/USD']
            },
            'scaling': {
                'current_tier': task_performance.get('scaling_status', {}).get('current_tier', 1),
                'next_threshold': task_performance.get('scaling_status', {}).get('next_threshold', 500),
                'auto_scaling': task_performance.get('scaling_status', {}).get('auto_scaling_active', False)
            }
        }
    
    async def process_chat_message(self, message: str, user_id: str = 'user') -> Dict[str, Any]:
        """Process chat message and potentially create tasks."""
        self.logger.info(f"Processing chat message: {message}")
        
        # Check if this is a task creation request
        task_keywords = ['create', 'start', 'begin', 'launch', 'execute', 'run']
        if any(keyword in message.lower() for keyword in task_keywords):
            if self.task_manager:
                # Process as task creation
                result = await self.task_manager.process_natural_language_task(message, user_id)
                
                # Update dashboard
                await self.send_dashboard_update()
                
                return {
                    'type': 'task_creation',
                    'response': f"Created {result['agents_created']} micro-agents for your task. Estimated revenue: ${result['estimated_revenue']:.2f}",
                    'task_result': result
                }
            else:
                return {
                    'type': 'error',
                    'response': 'Task manager not available. Please check system status.'
                }
        
        # Regular chat response
        return {
            'type': 'chat',
            'response': f"I understand you said: '{message}'. How can I help you with trading or task automation?"
        }
    
    def update_wallet_data(self, new_data: Dict[str, Any]):
        """Update wallet information."""
        self.wallet_data.update(new_data)
        
    def update_system_metrics(self, new_metrics: Dict[str, Any]):
        """Update system performance metrics."""
        self.system_metrics.update(new_metrics)

# Global dashboard manager instance
dashboard_manager = DashboardManager()

app = FastAPI(title="PhindLlama Dashboard API")

@app.websocket("/ws/dashboard")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time dashboard updates."""
    await dashboard_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data.get('type') == 'chat':
                # Process chat message
                response = await dashboard_manager.process_chat_message(
                    message_data.get('message', ''),
                    message_data.get('user_id', 'user')
                )
                await websocket.send_text(json.dumps({
                    'type': 'chat_response',
                    'data': response
                }))
            
    except WebSocketDisconnect:
        dashboard_manager.disconnect(websocket)

@app.get("/api/dashboard")
async def get_dashboard():
    """Get current dashboard data."""
    return await dashboard_manager.get_dashboard_data()

@app.post("/api/task")
async def create_task(task_data: Dict[str, Any]):
    """Create a new task via API."""
    if dashboard_manager.task_manager:
        result = await dashboard_manager.task_manager.process_natural_language_task(
            task_data.get('description', ''),
            task_data.get('user_id', 'api_user')
        )
        await dashboard_manager.send_dashboard_update()
        return result
    else:
        return {'error': 'Task manager not available'}

@app.get("/api/wallet")
async def get_wallet_info():
    """Get wallet configuration and status."""
    return {
        'balance': dashboard_manager.wallet_data['total_balance'],
        'positions': dashboard_manager.wallet_data['positions'],
        'configuration': {
            'risk_level': 'medium',
            'max_position_size': 0.1,
            'stop_loss': 0.05,
            'take_profit': 0.15
        },
        'supported_networks': ['Ethereum', 'Polygon', 'BSC', 'Arbitrum'],
        'connected_exchanges': ['Binance', 'Coinbase', 'Uniswap']
    }

@app.get("/api/profit")
async def get_profit():
    """Get profit and income tracking data."""
    return dashboard_manager.profit_monitor.get_profit_summary()

@app.post("/api/income/track")
async def track_income(income_data: Dict[str, Any]):
    """
    Track a new income event.
    
    Expected format:
    {
        "amount": 45.75,
        "source": "trading",
        "details": {"pair": "ETH/USDT", "strategy": "arbitrage"}
    }
    """
    try:
        amount = float(income_data.get("amount", 0))
        source = income_data.get("source", "unknown")
        details = income_data.get("details", {})
        
        if amount <= 0:
            return {"status": "error", "message": "Amount must be greater than zero"}
            
        dashboard_manager.profit_monitor.track_income(amount, source, details)
        await dashboard_manager.send_dashboard_update()
        
        return {
            "status": "success",
            "message": f"Income of ${amount:.2f} from {source} tracked successfully"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/expense/track")
async def track_expense(expense_data: Dict[str, Any]):
    """
    Track a new expense event.
    
    Expected format:
    {
        "amount": 12.50,
        "category": "infrastructure",
        "details": {"service": "cloud_run", "provider": "gcp"}
    }
    """
    try:
        amount = float(expense_data.get("amount", 0))
        category = expense_data.get("category", "unknown")
        details = expense_data.get("details", {})
        
        if amount <= 0:
            return {"status": "error", "message": "Amount must be greater than zero"}
            
        dashboard_manager.profit_monitor.track_expense(amount, category, details)
        await dashboard_manager.send_dashboard_update()
        
        return {
            "status": "success",
            "message": f"Expense of ${amount:.2f} for {category} tracked successfully"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
async def get_dashboard_ui():
    """Serve the dashboard UI."""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>PhindLlama Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #0f1419; color: #fff; }
            .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
            .card { background: #1e2328; border-radius: 8px; padding: 20px; border: 1px solid #2b3139; }
            .card h3 { margin-top: 0; color: #f0b90b; }
            .metric { display: flex; justify-content: space-between; margin: 10px 0; }
            .metric-value { font-weight: bold; color: #02c076; }
            .status-operational { color: #02c076; }
            .status-warning { color: #fcd535; }
            .chat-container { height: 300px; border: 1px solid #2b3139; border-radius: 4px; }
            .chat-messages { height: 240px; overflow-y: auto; padding: 10px; background: #0b0e11; }
            .chat-input { width: 100%; padding: 10px; background: #1e2328; border: none; color: #fff; }
            .task-item { background: #0b0e11; padding: 10px; margin: 5px 0; border-radius: 4px; }
            #status { position: fixed; top: 10px; right: 10px; padding: 10px; background: #02c076; border-radius: 4px; }
        </style>
    </head>
    <body>
        <div id="status">● CONNECTED</div>
        <h1>🚀 PhindLlama Autonomous Trading Dashboard</h1>
        
        <div class="dashboard">
            <div class="card">
                <h3>💰 Wallet & Revenue</h3>
                <div class="metric">
                    <span>Total Balance:</span>
                    <span class="metric-value" id="total-balance">$0.00</span>
                </div>
                <div class="metric">
                    <span>Daily Revenue:</span>
                    <span class="metric-value" id="daily-revenue">$0.00</span>
                </div>
                <div class="metric">
                    <span>Daily Target:</span>
                    <span id="daily-target">$200.00</span>
                </div>
                <div class="metric">
                    <span>Progress:</span>
                    <span id="progress">0%</span>
                </div>
                <div class="metric">
                    <span>Monthly Projection:</span>
                    <span class="metric-value" id="monthly-projection">$0.00</span>
                </div>
            </div>
            
            <div class="card">
                <h3>🤖 Agent Status</h3>
                <div class="metric">
                    <span>Active Agents:</span>
                    <span class="metric-value" id="active-agents">0</span>
                </div>
                <div class="metric">
                    <span>Completed Tasks:</span>
                    <span id="completed-tasks">0</span>
                </div>
                <div class="metric">
                    <span>Success Rate:</span>
                    <span class="metric-value" id="success-rate">0%</span>
                </div>
                <div class="metric">
                    <span>Auto-Scaling:</span>
                    <span id="auto-scaling" class="status-operational">ACTIVE</span>
                </div>
            </div>
            
            <div class="card">
                <h3>📊 System Status</h3>
                <div class="metric">
                    <span>Status:</span>
                    <span class="status-operational" id="system-status">OPERATIONAL</span>
                </div>
                <div class="metric">
                    <span>Uptime:</span>
                    <span id="uptime">0.0 hours</span>
                </div>
                <div class="metric">
                    <span>CPU Usage:</span>
                    <span id="cpu-usage">0%</span>
                </div>
                <div class="metric">
                    <span>Memory:</span>
                    <span id="memory-usage">0%</span>
                </div>
            </div>
            
            <div class="card">
                <h3>📈 Market Data</h3>
                <div class="metric">
                    <span>BTC/USD:</span>
                    <span class="metric-value" id="btc-price">$0.00</span>
                </div>
                <div class="metric">
                    <span>ETH/USD:</span>
                    <span class="metric-value" id="eth-price">$0.00</span>
                </div>
                <div class="metric">
                    <span>Volatility:</span>
                    <span id="volatility">0%</span>
                </div>
            </div>
            
            <div class="card">
                <h3>🎯 Active Tasks</h3>
                <div id="active-tasks-list">
                    <div class="task-item">No active tasks</div>
                </div>
            </div>
            
            <div class="card">
                <h3>💬 Chat Interface</h3>
                <div class="chat-container">
                    <div id="chat-messages" class="chat-messages">
                        <div>🤖 Hello! I can help you create trading tasks, analyze markets, or manage your portfolio. Try saying "create an arbitrage trading task" or "start yield farming".</div>
                    </div>
                    <input type="text" id="chat-input" class="chat-input" placeholder="Type a command or question..." />
                </div>
            </div>
        </div>
        
        <script>
            const ws = new WebSocket('ws://localhost:8000/ws/dashboard');
            
            ws.onopen = function(event) {
                document.getElementById('status').textContent = '● CONNECTED';
                document.getElementById('status').style.background = '#02c076';
            };
            
            ws.onclose = function(event) {
                document.getElementById('status').textContent = '● DISCONNECTED';
                document.getElementById('status').style.background = '#f6465d';
            };
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                
                if (data.timestamp) {
                    // Dashboard update
                    updateDashboard(data);
                } else if (data.type === 'chat_response') {
                    // Chat response
                    addChatMessage('🤖 ' + data.data.response);
                }
            };
            
            function updateDashboard(data) {
                // Update wallet info
                document.getElementById('total-balance').textContent = '$' + data.wallet.total_balance.toFixed(2);
                document.getElementById('daily-revenue').textContent = '$' + data.revenue.daily_actual.toFixed(2);
                document.getElementById('daily-target').textContent = '$' + data.revenue.daily_target.toFixed(2);
                document.getElementById('progress').textContent = data.revenue.progress_percent.toFixed(1) + '%';
                document.getElementById('monthly-projection').textContent = '$' + data.revenue.monthly_projection.toFixed(2);
                
                // Update agent info
                document.getElementById('active-agents').textContent = data.agents.active_count;
                document.getElementById('completed-tasks').textContent = data.agents.completed_tasks;
                document.getElementById('success-rate').textContent = (data.agents.success_rate * 100).toFixed(1) + '%';
                document.getElementById('auto-scaling').textContent = data.scaling.auto_scaling ? 'ACTIVE' : 'INACTIVE';
                
                // Update system info
                document.getElementById('system-status').textContent = data.system.status.toUpperCase();
                document.getElementById('uptime').textContent = data.system.uptime_hours.toFixed(1) + ' hours';
                document.getElementById('cpu-usage').textContent = data.system.cpu_usage + '%';
                document.getElementById('memory-usage').textContent = data.system.memory_usage + '%';
                
                // Update market data
                document.getElementById('btc-price').textContent = '$' + data.market.btc_price.toFixed(2);
                document.getElementById('eth-price').textContent = '$' + data.market.eth_price.toFixed(2);
                document.getElementById('volatility').textContent = (data.market.market_volatility * 100).toFixed(1) + '%';
                
                // Update active tasks
                updateActiveTasks(data.agents.active_tasks);
            }
            
            function updateActiveTasks(tasks) {
                const container = document.getElementById('active-tasks-list');
                if (tasks.length === 0) {
                    container.innerHTML = '<div class="task-item">No active tasks</div>';
                } else {
                    container.innerHTML = tasks.map(task => 
                        `<div class="task-item">
                            <strong>${task.type}</strong><br>
                            Status: ${task.status}<br>
                            Revenue: $${task.revenue_generated.toFixed(2)}
                        </div>`
                    ).join('');
                }
            }
            
            function addChatMessage(message) {
                const messages = document.getElementById('chat-messages');
                const div = document.createElement('div');
                div.textContent = message;
                div.style.margin = '5px 0';
                messages.appendChild(div);
                messages.scrollTop = messages.scrollHeight;
            }
            
            document.getElementById('chat-input').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    const message = this.value.trim();
                    if (message) {
                        addChatMessage('👤 ' + message);
                        ws.send(JSON.stringify({
                            type: 'chat',
                            message: message,
                            user_id: 'dashboard_user'
                        }));
                        this.value = '';
                    }
                }
            });
            
            // Request initial data every 5 seconds
            setInterval(() => {
                ws.send(JSON.stringify({type: 'ping'}));
            }, 5000);
        </script>
    </body>
    </html>
    """)
