import time
from web3 import Web3
from wallet.profit_tracker import WalletProfitTracker
from orchestrator import AdaptiveOrchestrator
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{os.getenv("INFURA_KEY")}'))
    tracker = WalletProfitTracker(w3, os.getenv("WALLET_ADDRESS"))
    orchestrator = AdaptiveOrchestrator(w3)
    
    while True:
        try:
            tracker.update_snapshot()
            orchestrator.run_cycle()
            time.sleep(3600)  # Run hourly
        except Exception as e:
            logging.error(f"Adaptation cycle failed: {str(e)}")
            time.sleep(300)  # Wait 5 minutes before retry

if __name__ == "__main__":
    main()