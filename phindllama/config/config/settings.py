"""Settings configuration for the application."""
from typing import Dict, Any

class Settings:
    """Settings manager for application configuration."""
    
    def __init__(self):
        """Initialize settings with default values."""
        self.config = {
            'llm': {
                'model_name': 'distilbert-base-uncased',
                'task': 'text-classification',
                'temperature': 0.7,
                'max_length': 100
            }
        }
    
    def get_default_settings(self) -> Dict[str, Any]:
        """Return default application settings.
        
        Returns:
            Dict[str, Any]: Dictionary containing default settings
        """
