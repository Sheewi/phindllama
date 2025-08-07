# app/marketing/grant_manager.py
from typing import Dict, Any, List
import requests
from datetime import datetime
import json
from app.storage.persistent_memory import PersistentMemory

class GrantManager:
    def __init__(self, memory: PersistentMemory):
        self.memory = memory
        self._initialize_grant_sources()
        
    def _initialize_grant_sources(self) -> None:
        """Initialize grant sources and their APIs."""
        self.grant_sources = {
            'startup_grants': {
                'url': 'https://api.startupgrants.com/v1/grants',
                'api_key': self._get_secret('STARTUP_GRANTS_API_KEY')
            },
            'crypto_grants': {
                'url': 'https://api.cryptogrants.org/v1/grants',
                'api_key': self._get_secret('CRYPTO_GRANTS_API_KEY')
            }
        }
        
    def _get_secret(self, secret_id: str) -> str:
        """Retrieve secret from secure storage."""
        return self.memory.redis_client.get(f"secrets:{secret_id}")
        
    def search_grants(self) -> List[Dict[str, Any]]:
        """Search for available grants."""
        grants = []
        for source, config in self.grant_sources.items():
            response = requests.get(
                config['url'],
                headers={'Authorization': f"Bearer {config['api_key']}"}
            )
            if response.status_code == 200:
                grants.extend(response.json()['grants'])
        return grants
        
    def apply_for_grant(self, grant: Dict[str, Any]) -> bool:
        """Automatically apply for a grant."""
        try:
            response = requests.post(
                grant['application_url'],
                json=self._prepare_application(grant),
                headers={'Authorization': f"Bearer {self.grant_sources['crypto_grants']['api_key']}"}
            )
            if response.status_code == 200:
                self.memory.store_grant_application(grant)
                return True
            return False
        except Exception as e:
            self.memory.log_error(f"Grant application failed: {str(e)}")
            return False
        
    def _prepare_application(self, grant: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare grant application data."""
        return {
            'project_name': 'PhindLLama',
            'description': 'AI-powered autonomous trading system',
            'amount_requested': grant['max_amount'],
            'use_case': 'Development of autonomous trading capabilities',
            'timeline': '6 months',
            'team_size': 1,
            'contact_info': self._get_contact_info()
        }