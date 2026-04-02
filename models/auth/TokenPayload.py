
from pydantic import BaseModel


class TokenPayload(BaseModel):
    """Claims stored inside a JWT."""

    email: str