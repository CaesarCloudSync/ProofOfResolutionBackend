
from pydantic import BaseModel

from models.blockchain.BlockDTO import BlockDTO


class GetChainResponse(BaseModel):
    """Response containing the full blockchain."""

    chain: list[BlockDTO]
    length: int

