# config/settings.py
"""Configuration with security and validation."""
from pydantic import BaseSettings, SecretStr
from typing import Dict, Any, Optional
import os

class Settings(BaseSettings):
    """Application settings with security features."""
    api_key: Optional[SecretStr]
    gcp_project: str
    model_bucket: str
    database_url: str
    logging_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        
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
