from pydantic import BaseModel


class Resolution(BaseModel):
    goal_id: str
    title: str
    description: str = ""
    category: str = "General"
    block_index: int
    block_hash: str