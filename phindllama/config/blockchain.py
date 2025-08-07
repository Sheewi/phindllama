from web3 import Web3
from .secrets import INFURA_KEY, WALLET_ADDRESS

def get_web3():
    """Initialize Web3 with fallback providers"""
    return Web3(Web3.HTTPProvider(
        f'https://mainnet.infura.io/v3/{INFURA_KEY}'
    ))

def validate_address(address: str) -> bool:
    return Web3.is_address(address)