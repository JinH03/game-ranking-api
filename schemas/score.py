from pydantic import BaseModel, Field, ConfigDict

class Score(BaseModel):
    name : str = Field(min_length=2)
    rating : int = Field( ge = 0 )


class Score_update(BaseModel):
    rating: int = Field(ge=0)


class ScoreResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id: int
    name: str
    rating: int

    

class ScoreListResponse(BaseModel):
    items: list[ScoreResponse]
    page: int
    limit: int
    total: int