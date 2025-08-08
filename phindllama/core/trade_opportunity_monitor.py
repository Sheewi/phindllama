"""
Trade opportunity alert system for PhindLlama
"""
import logging
import json
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import asyncio
import aiohttp
import os

logger = logging.getLogger(__name__)

class TradeOpportunityMonitor:
    """Monitors and alerts for trade opportunities."""
    
    def __init__(self):
        self.active_alerts: List[Dict[str, Any]] = []
        self.alert_thresholds = {
            "price_differential": 0.015,  # 1.5% price difference for arbitrage
            "volatility_min": 0.025,      # 2.5% minimum volatility for swing opportunities
            "trend_strength_min": 0.6,    # 0.6 minimum trend strength (0-1 scale)
            "volume_spike": 2.5           # 2.5x normal volume for volume-based opportunities
        }
        self.alert_channels = {
            "dashboard": True,
            "email": os.environ.get("ENABLE_EMAIL_ALERTS", "False").lower() == "true",
            "sms": os.environ.get("ENABLE_SMS_ALERTS", "False").lower() == "true",
            "webhooks": []
        }
        if webhook_url := os.environ.get("ALERT_WEBHOOK_URL"):
            self.alert_channels["webhooks"].append(webhook_url)
            
        # Track opportunities with IDs
        self.opportunity_counter = 0
        # Background runner control
        self._running = False
        self._background_task = None

    async def run_background_monitor(self, interval: float = 10.0):
        """Continuously monitor and assign microagents or generate income."""
        self._running = True
        logger.info("TradeOpportunityMonitor background loop started.")
        while self._running:
            try:
                # Example: Simulate opportunity detection (replace with real data source)
                # You could fetch market data here and evaluate opportunities
                dummy_data = {
                    "asset_pair": "BTC/USDT",
                    "exchange1": {"name": "Binance", "price": 65420.5},
                    "exchange2": {"name": "Coinbase", "price": 65550.0}
                }
                found, opportunity = self.evaluate_arbitrage_opportunity(dummy_data)
                if found and opportunity:
                    await self.send_alert(opportunity)
                    # Here you could trigger microagent assignment or income generation
                    logger.info(f"Microagent assigned for opportunity: {opportunity['id']}")
                # Add more opportunity checks as needed
            except Exception as e:
                logger.error(f"Error in background monitor: {str(e)}")
            await asyncio.sleep(interval)

    def start_background_monitor(self, interval: float = 10.0):
        """Start the background monitor as an asyncio task."""
        if not self._background_task:
            loop = asyncio.get_event_loop()
            self._background_task = loop.create_task(self.run_background_monitor(interval))

    def stop_background_monitor(self):
        """Stop the background monitor."""
        self._running = False
        if self._background_task:
            self._background_task.cancel()
            self._background_task = None
    
    def add_webhook(self, url: str) -> bool:
        """Add a webhook URL for opportunity alerts."""
        if url not in self.alert_channels["webhooks"]:
            self.alert_channels["webhooks"].append(url)
            return True
        return False
    
    def remove_webhook(self, url: str) -> bool:
        """Remove a webhook URL."""
        if url in self.alert_channels["webhooks"]:
            self.alert_channels["webhooks"].remove(url)
            return True
        return False
            
    def update_thresholds(self, new_thresholds: Dict[str, float]) -> Dict[str, float]:
        """Update alert thresholds."""
        self.alert_thresholds.update(new_thresholds)
        return self.alert_thresholds
    
    def evaluate_arbitrage_opportunity(self, data: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Evaluate arbitrage opportunity between exchanges."""
        asset_pair = data.get("asset_pair", "")
        exchange1 = data.get("exchange1", {})
        exchange2 = data.get("exchange2", {})
        
        # Verify required data
        if not asset_pair or not exchange1 or not exchange2:
            return False, None
            
        price1 = exchange1.get("price", 0)
        price2 = exchange2.get("price", 0)
        
        if price1 <= 0 or price2 <= 0:
            return False, None
            
        # Calculate price differential
        if price1 > price2:
            diff_percent = (price1 - price2) / price2
            buy_exchange = exchange2["name"]
            sell_exchange = exchange1["name"]
            buy_price = price2
            sell_price = price1
        else:
            diff_percent = (price2 - price1) / price1
            buy_exchange = exchange1["name"]
            sell_exchange = exchange2["name"] 
            buy_price = price1
            sell_price = price2
        
        # Check if differential exceeds threshold
        if diff_percent >= self.alert_thresholds["price_differential"]:
            opportunity = {
                "id": f"arb-{self.opportunity_counter}",
                "type": "arbitrage",
                "asset_pair": asset_pair,
                "buy_exchange": buy_exchange,
                "sell_exchange": sell_exchange,
                "buy_price": buy_price,
                "sell_price": sell_price,
                "differential_percent": diff_percent * 100,
                "estimated_profit": diff_percent - 0.002,  # Rough estimate accounting for fees
                "timestamp": datetime.now().isoformat(),
                "status": "detected",
                "risk_level": "low" if diff_percent < 0.03 else "medium",
                "action_items": [
                    f"Buy {asset_pair} on {buy_exchange} at ${buy_price:.2f}",
                    f"Sell {asset_pair} on {sell_exchange} at ${sell_price:.2f}"
                ]
            }
            self.opportunity_counter += 1
            return True, opportunity
        
        return False, None
        
    def evaluate_trend_opportunity(self, data: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Evaluate trend-based trading opportunity."""
        asset = data.get("asset", "")
        trend_strength = data.get("trend_strength", 0)
        direction = data.get("direction", "")
        price = data.get("price", 0)
        
        if not all([asset, trend_strength, direction, price]):
            return False, None
            
        if trend_strength >= self.alert_thresholds["trend_strength_min"]:
            opportunity = {
                "id": f"trend-{self.opportunity_counter}",
                "type": "trend",
                "asset": asset,
                "direction": direction,
                "price": price,
                "trend_strength": trend_strength,
                "timestamp": datetime.now().isoformat(),
                "status": "detected",
                "risk_level": "medium",
                "action_items": [
                    f"{'Buy' if direction == 'up' else 'Sell'} {asset} at ${price:.2f}"
                ]
            }
            self.opportunity_counter += 1
            return True, opportunity
            
        return False, None
    
    async def send_alert(self, opportunity: Dict[str, Any]) -> bool:
        """Send alert through configured channels."""
        alert_sent = False
        
        # Log the opportunity
        logger.info(f"Trade opportunity detected: {opportunity['type']} - {opportunity.get('asset_pair', opportunity.get('asset', 'unknown'))}")
        
        # Add to active alerts
        self.active_alerts.append(opportunity)
        if len(self.active_alerts) > 100:  # Prevent memory bloat
            self.active_alerts = self.active_alerts[-100:]
            
        # Send to webhooks if configured
        if self.alert_channels["webhooks"]:
            webhook_success = await self._send_webhook_alerts(opportunity)
            alert_sent = alert_sent or webhook_success
            
        return alert_sent
    
    async def _send_webhook_alerts(self, opportunity: Dict[str, Any]) -> bool:
        """Send alert to configured webhooks."""
        success = False
        
        for webhook_url in self.alert_channels["webhooks"]:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(webhook_url, json=opportunity) as response:
                        if response.status == 200:
                            logger.info(f"Alert sent successfully to webhook {webhook_url}")
                            success = True
                        else:
                            logger.warning(f"Failed to send alert to webhook {webhook_url}: {response.status}")
            except Exception as e:
                logger.error(f"Error sending webhook alert: {str(e)}")
                
        return success
    
    def get_active_opportunities(self, opportunity_type: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Get active trading opportunities."""
        if opportunity_type:
            filtered = [opp for opp in self.active_alerts if opp["type"] == opportunity_type]
            return filtered[:limit]
        return self.active_alerts[:limit]
    
    def get_opportunity_by_id(self, opp_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific opportunity by ID."""
        for opportunity in self.active_alerts:
            if opportunity["id"] == opp_id:
                return opportunity
        return None
    
    def mark_opportunity_actioned(self, opp_id: str, action: str = "actioned") -> bool:
        """Mark an opportunity as actioned or ignored."""
        for opportunity in self.active_alerts:
            if opportunity["id"] == opp_id:
                opportunity["status"] = action
                opportunity["actioned_at"] = datetime.now().isoformat()
                return True
        return False
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get a summary for the dashboard."""
        active_count = len([opp for opp in self.active_alerts if opp["status"] == "detected"])
        actioned_count = len([opp for opp in self.active_alerts if opp["status"] == "actioned"])
        ignored_count = len([opp for opp in self.active_alerts if opp["status"] == "ignored"])
        
        # Group by type
        types = {}
        for opp in self.active_alerts:
            opp_type = opp["type"]
            if opp_type not in types:
                types[opp_type] = 0
            types[opp_type] += 1
            
        return {
            "active_opportunities": active_count,
            "actioned_opportunities": actioned_count,
            "ignored_opportunities": ignored_count,
            "opportunity_types": types,
            "thresholds": self.alert_thresholds
        }

# Create singleton instance
opportunity_monitor = TradeOpportunityMonitor()
