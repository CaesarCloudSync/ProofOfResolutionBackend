

from pydantic import BaseModel


class TokenResponse(BaseModel):
    """JWT access token returned after successful login."""

    access_token: str
    token_type: str = "bearer"

