# src/config/settings.py
class Settings:
    def __init__(self):
        self.environment = None
        self.wallet_config = {}
        self.agent_configs = {}
        
    def load_from_env(self):
        """Load sensitive configurations from environment"""
        self.wallet_config['private_key'] = os.environ.get('WALLET_PRIVATE_KEY')
        self.wallet_config['api_keys'] = {
            key: os.environ.get(f'API_KEY_{key.upper()}')
            for key in ['EXCHANGE1', 'EXCHANGE2']
        }
