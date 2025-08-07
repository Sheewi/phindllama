from datetime import datetime, timedelta
import random

class FundRouter:
    def __init__(self):
        self.route_strategies = [
            self._direct_transfer,
            self._time_delayed,
            self._amount_split
        ]
    
    def route_to_main(self, source_wallet, target_amount):
        """Selects optimal routing strategy"""
        strategy = random.choice(self.route_strategies)
        return strategy(source_wallet, target_amount)
    
    def _direct_transfer(self, wallet, amount):
        """Simple direct transfer"""
        return [{
            'from': wallet['address'],
            'to': self.main_wallet,
            'amount': amount,
            'time': datetime.now()
        }]
    
    def _time_delayed(self, wallet, amount):
        """Split with time delays"""
        parts = self._split_amount(amount, 3)
        return [{
            'from': wallet['address'],
            'to': self.main_wallet,
            'amount': part,
            'time': datetime.now() + timedelta(minutes=i*15)y
