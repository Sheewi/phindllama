from web3 import Web3
import pandas as pd
from typing import List

class WalletProfitTracker:
    def __init__(self, w3: Web3, address: str):
        self.w3 = w3
        self.address = address
        self.history = pd.DataFrame(columns=[
            'timestamp', 'balance_eth', 'usd_value', 'tx_count'
        ])
        
    def update_snapshot(self):
        """Record wallet state"""
        balance = self.w3.eth.get_balance(self.address)
        new_row = {
            'timestamp': datetime.now(),
            'balance_eth': Web3.from_wei(balance, 'ether'),
            'usd_value': self._get_usd_value(balance),
            'tx_count': self._get_transaction_count()
        }
        self.history = pd.concat([
            self.history, 
            pd.DataFrame([new_row])
        ], ignore_index=True)
        
    def calculate_profitability(self, window: str = '7D') -> float:
        """ROI calculation over time window"""
        resampled = self.history.set_index('timestamp').resample(window)
        return (
            resampled['usd_value'].last() - 
            resampled['usd_value'].first()
        ) / resampled['usd_value'].first()