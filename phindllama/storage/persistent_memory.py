# phindllama/storage/persistent_memory.py
"""Persistent memory implementation for the phindllama system."""
from typing import Dict, Any, Optional
import json
from datetime import datetime, timedelta
import logging

# Try to import redis, fallback to in-memory storage
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

logger = logging.getLogger(__name__)

class PersistentMemory:
    """Persistent memory manager with Redis backend or in-memory fallback."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        
        if REDIS_AVAILABLE and self.config.get('use_redis', False):
            self._setup_redis()
        else:
            self._setup_memory()
        
        self._initialize_memory_spaces()
        
    def _setup_redis(self):
        """Setup Redis connection."""
        try:
            self.redis_client = redis.Redis(
                host=self.config.get('host', 'localhost'),
                port=self.config.get('port', 6379),
                db=self.config.get('db', 0),
                decode_responses=True
            )
            self.storage_type = 'redis'
            logger.info("Using Redis for persistent memory")
        except Exception as e:
            logger.warning(f"Redis setup failed, falling back to memory: {e}")
            self._setup_memory()
    
    def _setup_memory(self):
        """Setup in-memory storage."""
        self.memory_store = {}
        self.storage_type = 'memory'
        logger.info("Using in-memory storage for persistent memory")
        
    def _initialize_memory_spaces(self) -> None:
        """Initialize memory spaces for different data types."""
        self.memory_spaces = {
            'transactions': 'transactions:',
            'metrics': 'metrics:',
            'grants': 'grants:',
            'marketing': 'marketing:',
            'savings': 'savings:',
            'agents': 'agents:',
            'configs': 'configs:'
        }
        
    def store_transaction(self, tx_data: Dict[str, Any]) -> bool:
        """Store transaction data with TTL."""
        try:
            key = f"{self.memory_spaces['transactions']}{tx_data.get('tx_id', 'unknown')}"
            return self._store_data(key, tx_data)
        except Exception as e:
            logger.error(f"Error storing transaction: {e}")
            return False
    
    def get_transaction(self, tx_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve transaction data."""
        try:
            key = f"{self.memory_spaces['transactions']}{tx_id}"
            return self._get_data(key)
        except Exception as e:
            logger.error(f"Error retrieving transaction: {e}")
            return None
    
    def store_metric(self, metric_name: str, metric_data: Dict[str, Any]) -> bool:
        """Store metric data."""
        try:
            key = f"{self.memory_spaces['metrics']}{metric_name}"
            return self._store_data(key, metric_data)
        except Exception as e:
            logger.error(f"Error storing metric: {e}")
            return False
    
    def get_metric(self, metric_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve metric data."""
        try:
            key = f"{self.memory_spaces['metrics']}{metric_name}"
            return self._get_data(key)
        except Exception as e:
            logger.error(f"Error retrieving metric: {e}")
            return None
    
    def _store_data(self, key: str, data: Dict[str, Any]) -> bool:
        """Store data using the appropriate backend."""
        if self.storage_type == 'redis':
            try:
                serialized = json.dumps(data)
                self.redis_client.set(key, serialized)
                return True
            except Exception as e:
                logger.error(f"Redis store error: {e}")
                return False
        else:
            self.memory_store[key] = data
            return True
    
    def _get_data(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve data using the appropriate backend."""
        if self.storage_type == 'redis':
            try:
                data = self.redis_client.get(key)
                return json.loads(data) if data else None
            except Exception as e:
                logger.error(f"Redis get error: {e}")
                return None
        else:
            return self.memory_store.get(key)
    
    def get(self, key: str) -> Optional[Any]:
        """Generic get method."""
        return self._get_data(key)
    
    def set(self, key: str, value: Any) -> bool:
        """Generic set method."""
        if isinstance(value, dict):
            return self._store_data(key, value)
        else:
            # For non-dict values, wrap in a dict
            return self._store_data(key, {'value': value})
    
    def delete(self, key: str) -> bool:
        """Delete data."""
        if self.storage_type == 'redis':
            try:
                return bool(self.redis_client.delete(key))
            except Exception as e:
                logger.error(f"Redis delete error: {e}")
                return False
        else:
            return bool(self.memory_store.pop(key, None) is not None)
    
    def keys(self, pattern: str = "*") -> list:
        """List keys matching pattern."""
        if self.storage_type == 'redis':
            try:
                return self.redis_client.keys(pattern)
            except Exception as e:
                logger.error(f"Redis keys error: {e}")
                return []
        else:
            import fnmatch
            return [k for k in self.memory_store.keys() if fnmatch.fnmatch(k, pattern)]
    
    def flush(self) -> bool:
        """Clear all data."""
        if self.storage_type == 'redis':
            try:
                self.redis_client.flushdb()
                return True
            except Exception as e:
                logger.error(f"Redis flush error: {e}")
                return False
        else:
            self.memory_store.clear()
            return True
