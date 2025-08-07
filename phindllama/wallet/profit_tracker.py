from config.blockchain import get_web3, validate_address
from web3 import Web3
import pandas as pd
import os

class WalletProfitTracker:
    def __init__(self, w3: Web3 = None, address: str = None):
        self.w3 = w3 or get_web3()
        self.address = address or os.getenv('WALLET_ADDRESS')
        if not validate_address(self.address):
            raise ValueError("Invalid Ethereum address")
        
        self.history_file = os.path.join(
            os.path.dirname(__file__), 
            '../../data/wallet_history.csv'
        )
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)