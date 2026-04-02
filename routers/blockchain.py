"""Blockchain API router."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from BlockChain.BlockChain import BlockChain
from dependencies import get_blockchain
from models.blockchain.GetChainResponse import GetChainResponse
from models.blockchain.MineBlockResponse import MineBlockResponse
from models.blockchain.ValidityResponse import ValidityResponse

router = APIRouter(prefix="/blockchain", tags=["blockchain"])


@router.get(
    "/mine",
    response_model=MineBlockResponse,
    summary="Mine a new block",
)
def mine_block(blockchain: BlockChain = Depends(get_blockchain)) -> MineBlockResponse:
    """Perform proof-of-work and append a new block to the chain."""
    try:
        previous_block = blockchain.get_last_block()
        proof = blockchain.proof_of_work(previous_block.proof)
        previous_hash = blockchain.hash(previous_block)
        block = blockchain.create_block(proof, previous_hash)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    return MineBlockResponse(
        message="A block is MINED",
        index=block.index,
        timestamp=block.timestamp,
        proof=block.proof,
        previous_hash=block.previous_hash,
    )


@router.get(
    "/chain",
    response_model=GetChainResponse,
    summary="Retrieve the full chain",
)
def get_chain(blockchain: BlockChain = Depends(get_blockchain)) -> GetChainResponse:
    """Return every block in the chain in ascending order."""
    chain = blockchain.get_full_chain()
    return GetChainResponse(chain=chain, length=len(chain))


@router.get(
    "/valid",
    response_model=ValidityResponse,
    summary="Validate the chain",
)
def is_valid(blockchain: BlockChain = Depends(get_blockchain)) -> ValidityResponse:
    """Check whether the blockchain is internally consistent."""
    chain = blockchain.get_full_chain()
    valid = blockchain.chain_valid(chain)
    return ValidityResponse(
        message="The Blockchain is valid." if valid else "The Blockchain is not valid.",
        is_valid=valid,
    )