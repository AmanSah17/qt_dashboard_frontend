import requests
from typing import Optional, Dict, Any


class AuthClient:
    """HTTP client for authentication API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.user: Optional[Dict[str, Any]] = None

    def register(self, name: str, email: str, password: str) -> Dict[str, Any]:
        """Register a new user."""
        try:
            response = requests.post(
                f"{self.base_url}/register",
                json={"name": name, "email": email, "password": password},
                timeout=5
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login and get JWT token."""
        try:
            response = requests.post(
                f"{self.base_url}/login",
                json={"email": email, "password": password},
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            self.token = data.get("access_token")
            self.user = data.get("user")
            return {"success": True, "data": data}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify JWT token."""
        try:
            response = requests.get(
                f"{self.base_url}/verify",
                params={"token": token},
                timeout=5
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        if not self.token:
            return False
        result = self.verify_token(self.token)
        return result["success"]
