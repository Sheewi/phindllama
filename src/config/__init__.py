# src/config/__init__.py
"""Configuration module initialization."""
from pathlib import Path
import os
from typing import Dict, Any, Optional
from .settings import Settings
from .environment import EnvironmentConfig

def load_configuration(env_name: str = None) -> Dict[str, Any]:
    """
    Load configuration from environment variables and settings files.
    
    Args:
        env_name: Name of the environment to load
        
    Returns:
        Dictionary containing all configuration settings
    """
    settings = Settings()
    env_config = EnvironmentConfig(env_name or os.getenv('ENVIRONMENT', 'development'))
    
    # Merge configurations
    config = {**settings.get_default_settings(), **env_config.get_environment_settings()}
    
    # Override with environment variables
    for key, value in os.environ.items():
        if key.startswith('APP_'):
            config[key.replace('APP_', '').lower()] = value
            
    return config

def get_config_path(name: str) -> Optional[Path]:
    """Get path to configuration file."""
    base_dir = Path(__file__).parent
    config_path = base_dir / f"{name}.py"
    return config_path if config_path.exists() else None
