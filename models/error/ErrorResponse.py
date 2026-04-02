

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard error envelope."""

    detail: str
    status_code: int