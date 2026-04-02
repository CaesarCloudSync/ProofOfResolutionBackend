from pydantic import BaseModel


class ResolutionInfo(BaseModel):
    title: str
    description: str
    category: str