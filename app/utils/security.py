import os
from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from google.cloud import secretmanager

class AuthHandler:
    def __init__(self):
        self.client = secretmanager.SecretManagerServiceClient()
        self.api_key_name = os.getenv("API_KEY_NAME", "phindllama-api-key")
        
    async def get_secret(self, secret_id: str) -> str:
        name = f"projects/{os.getenv('GCP_PROJECT')}/secrets/{secret_id}/versions/latest"
        response = self.client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")

    async def validate_request(self, api_key: str = Depends(APIKeyHeader(name="x-api-key"))):
        stored_key = await self.get_secret(self.api_key_name)
        if api_key != stored_key:
            raise HTTPException(status_code=403, detail="Invalid API key")
