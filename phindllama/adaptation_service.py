import threading
import time
from web3 import Web3
from orchestrator import AdaptiveOrchestrator
import os
from dotenv import load_dotenv

load_dotenv()

class AdaptationService:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(
            f'https://mainnet.infura.io/v3/{os.getenv("INFURA_KEY")}'
        ))
        self.orchestrator = AdaptiveOrchestrator(self.w3)
        self.thread = threading.Thread(target=self.run, daemon=True)

    def run(self):
        while True:
            self.orchestrator.run_cycle()
            time.sleep(3600)  # Run every hour

    def start(self):
        self.thread.start()

if __name__ == "__main__":
    service = AdaptationService()
    service.start()
    service.thread.join()
