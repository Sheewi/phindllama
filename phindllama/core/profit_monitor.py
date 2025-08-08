#!/usr/bin/env python3
"""
Comprehensive profit monitoring and income tracking system for PhindLlama.
Tracks all revenue sources, calculates ROI, and projects future income.
"""

import os
import json
import logging
import datetime
from typing import Dict, List, Any, Optional
from google.cloud import pubsub_v1
from ..config.environment import get_environment_variable

logger = logging.getLogger(__name__)

class ProfitMonitor:
    """Tracks system income, expenses, and profitability metrics."""
    
    def __init__(self):
        """Initialize the profit monitoring system."""
        self.data_dir = os.path.join(os.path.dirname(__file__), '../../data')
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.income_file = os.path.join(self.data_dir, 'income_history.json')
        self.expenses_file = os.path.join(self.data_dir, 'expense_history.json')
        
        # Initialize tracking data
        self._load_data()
        
        # Cloud services setup
        self.project_id = get_environment_variable('GCP_PROJECT_ID', 'phind-468207')
        self.topic_name = get_environment_variable('INCOME_TOPIC', 'phindllama-income-events')
        self.publisher = self._setup_pubsub() if self.project_id else None
        
        self.daily_target = float(get_environment_variable('DAILY_REVENUE_TARGET', '200'))
        self.startup_date = datetime.datetime.now()
        
    def _setup_pubsub(self) -> Optional[pubsub_v1.PublisherClient]:
        """Set up Google Cloud Pub/Sub for income tracking."""
        try:
            return pubsub_v1.PublisherClient()
        except Exception as e:
            logger.warning(f"Failed to initialize Pub/Sub: {e}")
            return None
    
    def _load_data(self):
        """Load income and expense data from files."""
        if os.path.exists(self.income_file):
            try:
                with open(self.income_file, 'r') as f:
                    self.income_history = json.load(f)
            except Exception as e:
                logger.error(f"Error loading income data: {e}")
                self.income_history = {'entries': []}
        else:
            self.income_history = {'entries': []}
            
        if os.path.exists(self.expenses_file):
            try:
                with open(self.expenses_file, 'r') as f:
                    self.expense_history = json.load(f)
            except Exception as e:
                logger.error(f"Error loading expense data: {e}")
                self.expense_history = {'entries': []}
        else:
            self.expense_history = {'entries': []}
    
    def _save_data(self):
        """Save income and expense data to files."""
        try:
            with open(self.income_file, 'w') as f:
                json.dump(self.income_history, f, indent=2)
            
            with open(self.expenses_file, 'w') as f:
                json.dump(self.expense_history, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving profit tracking data: {e}")
    
    def track_income(self, amount: float, source: str, details: Dict[str, Any] = None):
        """
        Track a new income event.
        
        Args:
            amount: The income amount in USD
            source: Source of the income (e.g., 'trading', 'fees')
            details: Additional details about the income
        """
        now = datetime.datetime.now()
        
        # Create income entry
        entry = {
            'timestamp': now.isoformat(),
            'amount': amount,
            'source': source,
            'details': details or {},
            'date': now.strftime('%Y-%m-%d')
        }
        
        # Add to history
        self.income_history['entries'].append(entry)
        self._save_data()
        
        # Publish to Pub/Sub if available
        if self.publisher:
            try:
                topic_path = self.publisher.topic_path(self.project_id, self.topic_name)
                message_data = json.dumps(entry).encode('utf-8')
                self.publisher.publish(topic_path, data=message_data)
                logger.info(f"Published income event to {self.topic_name}: {amount:.2f} USD")
            except Exception as e:
                logger.error(f"Failed to publish to Pub/Sub: {e}")
    
    def track_expense(self, amount: float, category: str, details: Dict[str, Any] = None):
        """
        Track a new expense event.
        
        Args:
            amount: The expense amount in USD
            category: Category of expense (e.g., 'infrastructure', 'fees')
            details: Additional details about the expense
        """
        now = datetime.datetime.now()
        
        # Create expense entry
        entry = {
            'timestamp': now.isoformat(),
            'amount': amount,
            'category': category,
            'details': details or {},
            'date': now.strftime('%Y-%m-%d')
        }
        
        # Add to history
        self.expense_history['entries'].append(entry)
        self._save_data()
    
    def get_daily_income(self, date: str = None) -> float:
        """Get total income for a specific day."""
        date = date or datetime.datetime.now().strftime('%Y-%m-%d')
        
        total = 0.0
        for entry in self.income_history['entries']:
            if entry['date'] == date:
                total += entry['amount']
        
        return total
    
    def get_daily_expense(self, date: str = None) -> float:
        """Get total expenses for a specific day."""
        date = date or datetime.datetime.now().strftime('%Y-%m-%d')
        
        total = 0.0
        for entry in self.expense_history['entries']:
            if entry['date'] == date:
                total += entry['amount']
        
        return total
    
    def get_income_by_source(self) -> Dict[str, float]:
        """Get income breakdown by source."""
        result = {}
        for entry in self.income_history['entries']:
            source = entry['source']
            result[source] = result.get(source, 0) + entry['amount']
        
        return result
    
    def get_expense_by_category(self) -> Dict[str, float]:
        """Get expense breakdown by category."""
        result = {}
        for entry in self.expense_history['entries']:
            category = entry['category']
            result[category] = result.get(category, 0) + entry['amount']
        
        return result
    
    def get_profit_summary(self) -> Dict[str, Any]:
        """Get comprehensive profit summary."""
        now = datetime.datetime.now()
        today = now.strftime('%Y-%m-%d')
        
        # Calculate daily metrics
        daily_income = self.get_daily_income(today)
        daily_expense = self.get_daily_expense(today)
        daily_profit = daily_income - daily_expense
        
        # Calculate total metrics
        total_income = sum(entry['amount'] for entry in self.income_history['entries'])
        total_expense = sum(entry['amount'] for entry in self.expense_history['entries'])
        total_profit = total_income - total_expense
        
        # Calculate projections
        days_running = (now - self.startup_date).days + 1
        if days_running < 1:
            days_running = 1
            
        daily_average = total_income / days_running
        weekly_projection = daily_average * 7
        monthly_projection = daily_average * 30
        annual_projection = daily_average * 365
        
        # Calculate ROI metrics
        daily_roi = (daily_profit / daily_expense) * 100 if daily_expense > 0 else 0
        total_roi = (total_profit / total_expense) * 100 if total_expense > 0 else 0
        
        # Calculate target achievement
        daily_target_percent = (daily_income / self.daily_target) * 100 if self.daily_target > 0 else 0
        
        return {
            'date': today,
            'daily': {
                'income': daily_income,
                'expense': daily_expense,
                'profit': daily_profit,
                'roi_percent': daily_roi,
                'target_achievement_percent': daily_target_percent
            },
            'total': {
                'income': total_income,
                'expense': total_expense,
                'profit': total_profit,
                'roi_percent': total_roi
            },
            'projections': {
                'daily_average': daily_average,
                'weekly': weekly_projection,
                'monthly': monthly_projection,
                'annual': annual_projection
            },
            'breakdown': {
                'income_by_source': self.get_income_by_source(),
                'expense_by_category': self.get_expense_by_category()
            }
        }
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get dashboard-optimized income and profit data."""
        summary = self.get_profit_summary()
        
        # Format for dashboard display
        return {
            'daily_income': round(summary['daily']['income'], 2),
            'daily_profit': round(summary['daily']['profit'], 2),
            'total_profit': round(summary['total']['profit'], 2),
            'target_achievement': round(summary['daily']['target_achievement_percent'], 1),
            'daily_roi': round(summary['daily']['roi_percent'], 1),
            'total_roi': round(summary['total']['roi_percent'], 1),
            'monthly_projection': round(summary['projections']['monthly'], 2),
            'annual_projection': round(summary['projections']['annual'], 2),
            'top_income_sources': sorted(
                [(k, v) for k, v in summary['breakdown']['income_by_source'].items()],
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }

# Singleton instance
profit_monitor = ProfitMonitor()