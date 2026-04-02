from pydantic import BaseModel
from models.resolutions.dto.ResolutionInfo import ResolutionInfo
from models.blockchain.BlockDTO import BlockDTO


class CreateResolutionResponse(BaseModel):
    message: str
    goal_id: str
    resolution: ResolutionInfo
    block: BlockDTO