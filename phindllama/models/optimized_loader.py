import mmap
import os
from pathlib import Path
from typing import Optional
from loguru import logger
from app.security import AuthHandler

auth = AuthHandler()

class ModelLoader:
    def __init__(self):
        self.model_path = Path(os.getenv("MODEL_PATH"))
        self._model = None
        
    @property
    def model(self):
        if self._model is None:
            self._warmup()
        return self._model

    def _warmup(self):
        """Memory-mapped loading with validation"""
        if not self.model_path.exists():
            logger.error(f"Model not found at {self.model_path}")
            raise FileNotFoundError
            
        with open(self.model_path, "rb") as f:
            self._model = mmap.mmap(f.fileno(), 0, access=mmap.PROT_READ)
        logger.success(f"Loaded {self.model_path.name} ({self._model.size()/1e9:.2f}GB)")

    async def unload(self):
        if self._model:
            self._model.close()
            self._model = None