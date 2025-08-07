# config/security.py
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from jose import jwt
from datetime import datetime, timedelta
import os
from google.oauth2 import service_account
from google.cloud import secretmanager

class SecurityConfig:
    def __init__(self):
        self.api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        self._initialize_secret_manager()
        
    def _initialize_secret_manager(self):
        """Initialize Google Cloud Secret Manager."""
        credentials = service_account.Credentials.from_service_account_file(
            os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        )
        self.client = secretmanager.SecretManagerServiceClient(credentials=credentials)
        
    def get_secret(self, secret_id: str) -> str:
        """Retrieve secret from Secret Manager."""
        request = secretmanager.AccessSecretVersionRequest(
            name=f"projects/{os.environ.get('GCP_PROJECT')}/secrets/{secret_id}/versions/latest"
        )
        response = self.client.access_secret_version(request)
        return response.payload.data.decode("UTF-8")
        
    def validate_api_key(self, api_key: str = Security(api_key_header)) -> bool:
        """Validate API key against Secret Manager."""
        expected_key = self.get_secret("API_KEY")
        return api_key == expected_key
        