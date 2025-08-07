# config/settings.py
"""Configuration with security and validation."""
from pydantic import SecretStr
from typing import Dict, Any, Optional
import os

class Settings:
    """Application settings with security features."""
    
    def __init__(self):
        self.api_key: Optional[SecretStr] = None
        self.gcp_project: str = os.getenv('GCP_PROJECT', 'default')
        self.model_bucket: str = os.getenv('MODEL_BUCKET', 'default')
        self.database_url: str = os.getenv('DATABASE_URL', 'sqlite:///default.db')
        self.logging_level: str = os.getenv('LOGGING_LEVEL', 'INFO')
    
    def get_default_settings(self) -> Dict[str, Any]:
        """Get default settings dictionary."""
        return {
            'error_handling': {
                'max_retries': 3,
                'timeout': 30,
                'escalation_threshold': 5
            },
            'scaling': {
                'min_instances': 1,
                'max_instances': 10,
                'scale_factor': 1.5,
                'web': {
                    'traffic_threshold': 1000,
                    'response_time_threshold': 500
                }
            },
            'mcp': {
                'max_agents': 50,
                'agent_timeout': 60
            },
            'risk_management': {
                'max_position_size': 1000.0,
                'risk_threshold': 0.05
            }
        }
        
    @property
    def database_config(self) -> Dict[str, Any]:
        """Parse database URL with security."""
        from urllib.parse import urlparse
        parsed = urlparse(self.database_url)
        return {
            "host": parsed.hostname,
            "port": parsed.port,
            "database": parsed.path.strip("/"),
            "username": parsed.username,
            "password": parsed.password,
            "ssl": bool(parsed.scheme == "postgresql+psycopg2")
        }
