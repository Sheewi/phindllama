# phindllama/utils/payment_processor.py
"""Payment processing utilities for the phindllama system."""
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
from decimal import Decimal

logger = logging.getLogger(__name__)

class PaymentProcessor:
    """Payment processor for handling transactions and rewards."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get('enabled', False)
        self.supported_currencies = config.get('currencies', ['ETH', 'USD'])
        self.transaction_history = []
        
    def process_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a payment transaction."""
        try:
            amount = Decimal(str(payment_data.get('amount', 0)))
            currency = payment_data.get('currency', 'ETH')
            
            if currency not in self.supported_currencies:
                raise ValueError(f"Unsupported currency: {currency}")
            
            transaction = {
                'id': f"tx_{len(self.transaction_history):06d}",
                'amount': amount,
                'currency': currency,
                'type': payment_data.get('type', 'payment'),
                'status': 'completed' if self.enabled else 'simulated',
                'timestamp': datetime.now().isoformat(),
                'from': payment_data.get('from', 'unknown'),
                'to': payment_data.get('to', 'system')
            }
            
            self.transaction_history.append(transaction)
            
            return {
                'success': True,
                'transaction': transaction,
                'balance_updated': True
            }
            
        except Exception as e:
            logger.error(f"Payment processing error: {e}")
            return {
                'success': False,
                'error': str(e),
                'transaction': None
            }
    
    def generate_reward(self, reward_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate reward for completed tasks."""
        try:
            amount = Decimal(str(reward_data.get('amount', 0.001)))  # Default small reward
            currency = reward_data.get('currency', 'ETH')
            reason = reward_data.get('reason', 'task_completion')
            
            reward_transaction = {
                'id': f"reward_{len(self.transaction_history):06d}",
                'amount': amount,
                'currency': currency,
                'type': 'reward',
                'reason': reason,
                'status': 'completed' if self.enabled else 'simulated',
                'timestamp': datetime.now().isoformat(),
                'recipient': reward_data.get('recipient', 'system')
            }
            
            self.transaction_history.append(reward_transaction)
            
            return {
                'success': True,
                'reward': reward_transaction,
                'message': f"Reward of {amount} {currency} generated for {reason}"
            }
            
        except Exception as e:
            logger.error(f"Reward generation error: {e}")
            return {
                'success': False,
                'error': str(e),
                'reward': None
            }
    
    def get_balance(self, currency: str = 'ETH') -> Dict[str, Any]:
        """Get current balance for a currency."""
        total = Decimal('0')
        
        for tx in self.transaction_history:
            if tx['currency'] == currency and tx['status'] == 'completed':
                if tx['type'] == 'reward':
                    total += tx['amount']
                elif tx['type'] == 'payment' and tx['to'] == 'system':
                    total += tx['amount']
                elif tx['type'] == 'payment' and tx['from'] == 'system':
                    total -= tx['amount']
        
        return {
            'currency': currency,
            'balance': total,
            'last_updated': datetime.now().isoformat()
        }
    
    def get_transaction_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent transaction history."""
        return self.transaction_history[-limit:] if self.transaction_history else []
    
    def validate_transaction(self, tx_data: Dict[str, Any]) -> bool:
        """Validate transaction data."""
        required_fields = ['amount', 'currency']
        return all(field in tx_data for field in required_fields)
