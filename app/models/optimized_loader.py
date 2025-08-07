# app/models/optimized_loader.py
import mmap
import os
from typing import Dict, Any
from google.cloud import storage
from datetime import datetime, timedelta

class OptimizedModelLoader:
    def __init__(self, model_path: str, cache_duration: timedelta = timedelta(hours=24)):
        self.model_path = model_path
        self.cache_duration = cache_duration
        self._cache_path = f"/tmp/{os.path.basename(model_path)}"
        self._last_load_time = None
        self._memory_map = None
        
    def _memory_map_model(self) -> None:
        """Memory map model file for faster access."""
        with open(self._cache_path, "rb") as f:
            self._memory_map = mmap.mmap(
                f.fileno(),
                0,
                access=mmap.ACCESS_READ
            )
            
    def load_model(self) -> Any:
        """Load model with memory mapping and caching."""
        if self._should_refresh_cache():
            self._download_and_cache()
            self._memory_map_model()
            self._last_load_time = datetime.now()
            
        return self._load_from_memory_map()
        
    def _should_refresh_cache(self) -> bool:
        """Check if cache needs to be refreshed."""
        if not self._last_load_time:
            return True
        return datetime.now() - self._last_load_time > self.cache_duration