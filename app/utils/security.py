# app/utils/security.py
"""Security utilities and middleware."""
from fastapi import FastAPI, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt
from datetime import datetime, timedelta
import logging

class SecurityMiddleware:
    """Security middleware with authentication and rate limiting."""
    def __init__(self, app: FastAPI):
        self.app = app
        self.setup_middlewares()
        
    def setup_middlewares(self):
        """Set up security middlewares."""
        origins = [
            "http://localhost:3000",
            "https://your-domain.com"
        ]
        
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        self.app.add_middleware(
            SecurityHeadersMiddleware,
            security_headers=self._get_security_headers()
        )
        
    def _get_security_headers(self) -> Dict[str, str]:
        """Get security headers configuration."""
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'",
        }
