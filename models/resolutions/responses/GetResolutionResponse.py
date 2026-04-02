from pydantic import BaseModel
from models.resolutions.dto.Resolution import Resolution


class GetResolutionResponse(BaseModel):
    message: str
    resolution: Resolution