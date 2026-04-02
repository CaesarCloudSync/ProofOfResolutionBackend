
from pydantic import BaseModel


class ValidityResponse(BaseModel):
    """Response indicating whether the blockchain is valid."""

    message: str
    is_valid: bool

