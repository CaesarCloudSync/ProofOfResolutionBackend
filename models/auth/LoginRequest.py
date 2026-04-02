
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Payload for an authentication request."""

    email: str = Field(..., description="User email address")
    password: str = Field(..., description="Plain-text password (hashed server-side)")
