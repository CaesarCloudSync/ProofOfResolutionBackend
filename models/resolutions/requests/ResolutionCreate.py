from typing import Optional
from pydantic import BaseModel


class ResolutionCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    category: Optional[str] = "General"