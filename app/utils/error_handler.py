# app/utils/error_handler.py
"""Error handling and monitoring utilities."""
from typing import Dict, Any
import logging
from google.cloud import logging as cloud_logging
from fastapi import Request
from fastapi.responses import JSONResponse

class ErrorHandler:
    """Error handling with monitoring integration."""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cloud_logger = cloud_logging.Client().logger('app-errors')
        
    def handle_error(self, error: Exception, request: Request = None) -> JSONResponse:
        """Handle errors with monitoring and logging."""
        error_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(error),
            "request": {
                "method": request.method,
                "path": request.url.path
            } if request else None
        }
        
        self._log_to_cloud(error_data)
        self._log_locally(error_data)
        
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"},
            media_type="application/json"
        )
        
    def _log_to_cloud(self, error_data: Dict[str, Any]) -> None:
        """Log error to Cloud Logging."""
        try:
            self.cloud_logger.log_struct(error_data)
        except Exception as e:
            self.logger.error(f"Cloud logging failed: {str(e)}")
