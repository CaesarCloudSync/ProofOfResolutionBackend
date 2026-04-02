"""Resolution Service – business logic layer."""

from __future__ import annotations

from BlockChain.BlockChain import BlockChain
from models.blockchain.BlockDTO import BlockDTO
from models.resolutions.dto.Resolution import Resolution
from models.resolutions.dto.ResolutionInfo import ResolutionInfo
from models.resolutions.requests.ResolutionCreate import ResolutionCreate
from models.resolutions.responses.CreateResolutionResponse import CreateResolutionResponse
from repositories.ResolutionRepository import ResolutionRepository


class ResolutionService:
    """Orchestrates blockchain mining and database persistence for resolutions."""

    def __init__(self, blockchain: BlockChain, repository: ResolutionRepository) -> None:
        self.blockchain = blockchain
        self.repository = repository

    def create_resolution(self, resolution: ResolutionCreate) -> CreateResolutionResponse:
        """
        1. Mine a new block
        2. Persist the resolution linked to that block
        3. Return the combined response
        """
        block = self.blockchain.mine_block()
        block_hash = self.blockchain.hash(block)

        db_resolution = self.repository.create(
            title=resolution.title,
            description=resolution.description or "",
            category=resolution.category or "General",
            block_index=block.index,
            block_hash=block_hash,
        )

        return CreateResolutionResponse(
            message="🎉 Resolution locked on the blockchain! You've made a commitment to the universe.",
            goal_id=db_resolution.goal_id,
            resolution=ResolutionInfo(
                title=db_resolution.title,
                description=db_resolution.description,
                category=db_resolution.category,
            ),
            block=BlockDTO(
                index=block.index,
                proof=block.proof,
                previous_hash=block.previous_hash,
                block_hash=block.block_hash,
                timestamp=block.timestamp,
            ),
        )

    def get_all_resolutions(self) -> list[Resolution]:
        return self.repository.get_all()

    def get_resolution(self, goal_id: str) -> Resolution | None:
        return self.repository.get_by_id(goal_id)