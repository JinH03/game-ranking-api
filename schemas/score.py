from pydantic import BaseModel, Field

class Score(BaseModel):
    name : str = Field(min_length=2)
    rating : int = Field( ge = 0 )


class Score_update(BaseModel):
    rating: int = Field(ge=0)

