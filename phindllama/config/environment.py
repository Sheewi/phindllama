# src/config/environment.py
"""Environment-specific configurations."""
from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from .settings import Settings

class EnvironmentConfig:
    """
    Handles environment-specific configurations.
    
    Loads and manages different configurations based on deployment environment.
    """
    ENVIRONMENTS = ['development', 'staging', 'production']
    
    def __init__(self, env_name: str):
        if env_name not in self.ENVIRONMENTS:
            raise ValueError(f"Invalid environment: {env_name}. "
                           f"Must be one of: {self.ENVIRONMENTS}")
        
        self.env_name = env_name
        self.settings = Settings()
        
    def get_environment_settings(self) -> Dict[str, Any]:
        """Load environment-specific settings."""
        env_file = self._get_environment_file()
        if env_file:
            with open(env_file) as f:
                return yaml.safe_load(f)
        
        return self._get_default_env_settings()
    
    def _get_environment_file(self) -> Optional[Path]:
        """Get path to environment-specific configuration file."""
        base_dir = Path(__file__).parent
        env_file = base_dir / f"{self.env_name}.yaml"
        return env_file if env_file.exists() else None
    
    def _get_default_env_settings(self) -> Dict[str, Any]:
        """Return default settings for environment."""
        defaults = {
            'development': {
                'debug_mode': True,
                'mock_services': True,
                'wallet': {'testnet': True}
            },
            'staging': {
                'debug_mode': False,
                'mock_services': False,
                'wallet': {'testnet': True}
            },
            'production': {
                'debug_mode': False,
                'mock_services': False,
                'wallet': {'testnet': False}
            }
        }
        
        return defaults.get(self.env_name, {})

import os

def get_environment_variable(key: str, default: Any = None) -> Any:
    """
    Get value from environment variable.
    
    Args:
        key: Environment variable key
        default: Default value if not found
        
    Returns:
        Value from environment or default
    """
    return os.environ.get(key, default)
