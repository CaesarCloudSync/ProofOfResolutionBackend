from pydantic import BaseModel
from models.resolutions.dto.Resolution import Resolution


class GetAllResolutionsResponse(BaseModel):
    message: str
    resolutions: list[Resolution]
    total: int