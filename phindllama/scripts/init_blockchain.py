from config.blockchain import get_web3
from wallet.profit_tracker import WalletProfitTracker

def initialize():
    w3 = get_web3()
    if not w3.is_connected():
        raise ConnectionError("Failed to connect to blockchain")
    
    tracker = WalletProfitTracker(w3)
    tracker.update_snapshot()
    print(f"Initialized wallet tracker for {tracker.address}")

if __name__ == "__main__":
    initialize()