from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=2)
    password: str = Field(min_length=4)


class UserResponse(BaseModel):
    id: int
    username: str