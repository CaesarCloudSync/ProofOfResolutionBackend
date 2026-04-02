
from datetime import datetime

from pydantic import BaseModel


class MineBlockResponse(BaseModel):
    """Response returned after successfully mining a new block."""

    message: str
    index: int
    timestamp: datetime
    proof: int
    previous_hash: str

