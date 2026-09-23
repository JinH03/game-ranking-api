from pydantic import BaseModel, Field

class Score(BaseModel):
    name : str = Field(min_length=2)
    rating : int = Field( ge = 0 )


class Score_update(BaseModel):
    rating: int = Field(ge=0)


class ScoreResponse(BaseModel):
    id: int
    name: str
    rating: int

    class Config:
        from_attributes = True

class ScoreListResponse(BaseModel):
    items: list[ScoreResponse]
    page: int
    limit: int
    total: int