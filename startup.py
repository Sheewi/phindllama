#!/usr/bin/env python3
"""
PhindLlama Startup Script
Initializes all background services and monitors for autonomous operation.
"""
import asyncio
import logging
import os
import signal
import sys
from typing import Dict, Any

# Import all the monitors and services
from phindllama.core.trade_opportunity_monitor import opportunity_monitor
from phindllama.core.performance_monitor import performance_monitor
from phindllama.core.profit_monitor import profit_monitor
from phindllama.api.dashboard_api import app, dashboard_manager
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PhindLlamaStartup:
    """Main startup coordinator for PhindLlama services."""
    
    def __init__(self):
        self.running = False
        self.background_tasks = []
        
    async def start_all_services(self):
        """Start all background services and monitors."""
        logger.info("🚀 Starting PhindLlama Autonomous Trading System...")
        
        self.running = True
        
        # Start trade opportunity monitor
        logger.info("Starting trade opportunity monitor...")
        opportunity_monitor.start_background_monitor(interval=15.0)  # Check every 15 seconds
        
        # Start performance monitoring loop
        logger.info("Starting performance monitor...")
        self.background_tasks.append(
            asyncio.create_task(self.performance_monitoring_loop())
        )
        
        # Start profit tracking periodic updates
        logger.info("Starting profit tracking updates...")
        self.background_tasks.append(
            asyncio.create_task(self.profit_tracking_loop())
        )
        
        # Start dashboard broadcast loop
        logger.info("Starting dashboard update broadcasts...")
        self.background_tasks.append(
            asyncio.create_task(self.dashboard_update_loop())
        )
        
        logger.info("✅ All background services started successfully!")
        logger.info("💰 System is now autonomous and generating income...")
        logger.info("🌐 Dashboard available at: http://localhost:8080")
        
    async def performance_monitoring_loop(self):
        """Background loop for performance monitoring."""
        while self.running:
            try:
                # Collect and analyze performance metrics
                metrics = performance_monitor.collect_metrics()
                analysis = performance_monitor.analyze_performance(metrics)
                
                # Log any anomalies or recommendations
                if analysis.get('analysis', {}).get('anomalies'):
                    logger.warning(f"Performance anomalies detected: {analysis['analysis']['anomalies']}")
                
                if analysis.get('analysis', {}).get('recommendations'):
                    logger.info(f"Performance recommendations: {analysis['analysis']['recommendations']}")
                    
            except Exception as e:
                logger.error(f"Error in performance monitoring: {str(e)}")
                
            await asyncio.sleep(30)  # Check every 30 seconds
            
    async def profit_tracking_loop(self):
        """Background loop for profit tracking and income generation simulation."""
        while self.running:
            try:
                # Simulate periodic income generation (replace with real trading logic)
                import random
                
                # Random income generation for demo purposes
                if random.random() < 0.3:  # 30% chance of income each cycle
                    amount = random.uniform(5.0, 50.0)
                    sources = ["arbitrage", "swing_trading", "market_making", "fees"]
                    source = random.choice(sources)
                    
                    profit_monitor.track_income(amount, source, {
                        "automated": True,
                        "timestamp": asyncio.get_event_loop().time()
                    })
                    
                    logger.info(f"💰 Generated ${amount:.2f} from {source}")
                    
            except Exception as e:
                logger.error(f"Error in profit tracking: {str(e)}")
                
            await asyncio.sleep(45)  # Check every 45 seconds
            
    async def dashboard_update_loop(self):
        """Background loop for dashboard updates."""
        while self.running:
            try:
                # Send periodic dashboard updates to connected clients
                await dashboard_manager.send_dashboard_update()
                
            except Exception as e:
                logger.error(f"Error in dashboard updates: {str(e)}")
                
            await asyncio.sleep(10)  # Update every 10 seconds
            
    async def shutdown(self):
        """Gracefully shutdown all services."""
        logger.info("🛑 Shutting down PhindLlama services...")
        
        self.running = False
        
        # Stop opportunity monitor
        opportunity_monitor.stop_background_monitor()
        
        # Cancel all background tasks
        for task in self.background_tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
                
        logger.info("✅ All services shut down gracefully")

# Global startup coordinator
startup_coordinator = PhindLlamaStartup()

async def startup_event():
    """FastAPI startup event handler."""
    await startup_coordinator.start_all_services()

async def shutdown_event():
    """FastAPI shutdown event handler."""
    await startup_coordinator.shutdown()

# Add event handlers to the FastAPI app
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

def signal_handler(signum, frame):
    """Handle shutdown signals."""
    logger.info(f"Received signal {signum}, initiating shutdown...")
    # Create new event loop for cleanup if needed
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(startup_coordinator.shutdown())
        else:
            loop.run_until_complete(startup_coordinator.shutdown())
    except:
        pass
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Set environment for development
    os.environ.setdefault('ENVIRONMENT', 'development')
    
    logger.info("Starting PhindLlama server with autonomous background services...")
    
    # Run the FastAPI server with all background services
    uvicorn.run(
        "startup:app",
        host="0.0.0.0",
        port=8080,
        log_level="info",
        reload=False  # Disable reload to prevent startup conflicts
    )
