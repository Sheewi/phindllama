# app/models/model_manager.py
"""Model management with caching and security."""
from google.cloud import storage
import os
from typing import Dict, Any
from datetime import datetime, timedelta
import logging

class ModelLoader:
    def __init__(self, model_path: str, cache_duration: timedelta = timedelta(hours=24)):
        self.model_path = model_path
        self.cache_duration = cache_duration
        self.logger = logging.getLogger(__name__)
        self._cache_path = f"/tmp/{os.path.basename(model_path)}"
        self._last_load_time = None
        
    def load_from_gcs(self, bucket_name: str) -> Any:
        """Load model with local caching and security checks."""
        try:
            if self._should_refresh_cache():
                self._download_model(bucket_name)
                self._last_load_time = datetime.now()
            
            return self._load_model(self._cache_path)
        except Exception as e:
            self.logger.error(f"Model loading failed: {str(e)}")
            raise
            
    def _should_refresh_cache(self) -> bool:
        """Check if cache needs to be refreshed."""
        if not self._last_load_time:
            return True
        return datetime.now() - self._last_load_time > self.cache_duration
