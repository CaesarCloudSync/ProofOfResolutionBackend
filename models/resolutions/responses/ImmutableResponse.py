from pydantic import BaseModel


class ImmutableResponse(BaseModel):
    message: str
    tip: str
    goal_id: str