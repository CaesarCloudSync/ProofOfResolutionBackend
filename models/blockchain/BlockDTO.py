from datetime import datetime
from pydantic import BaseModel, Field


class BlockDTO(BaseModel):
    """Represents a single block in the chain."""

    index: int = Field(..., description="Block position in the chain")
    timestamp: datetime = Field(..., description="UTC timestamp of block creation")
    proof: int = Field(..., description="Proof-of-work value")
    previous_hash: str = Field(..., description="SHA-256 hash of the previous block")
    block_hash: str = Field(..., description="SHA-256 hash of this block's content")

    model_config = {"from_attributes": True}