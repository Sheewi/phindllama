# src/__init__.py
"""Main package initialization for the autonomous financial system."""
from pathlib import Path
import sys

# Add project root to path for relative imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

__version__ = "1.0.0"
__author__ = "Your Name"

def get_project_root() -> Path:
    """Get the project root directory."""
    return PROJECT_ROOT

def setup_logging():
    """Initialize logging configuration."""
    import logging.config
    
    logging_config = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'formatter': 'default'
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': 'app.log',
                'formatter': 'default'
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
    
    logging.config.dictConfig(logging_config)
    return logging.getLogger(__name__)

# Initialize logging
logger = setup_logging()
