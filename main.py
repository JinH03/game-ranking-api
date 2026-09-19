from fastapi import FastAPI, Path
from fastapi import HTTPException, Query
from pydantic import BaseModel, Field


app = FastAPI()
class Score(BaseModel):
    name : str = Field(min_length=2)
    rating : int = Field( ge = 0 )


class Score_update(BaseModel):
    rating: int = Field(ge=0)


game_scores = [
    {"name": "Player1", "rating": 1500},
    {"name": "Player2", "rating": 1200},
    {"name": "Player3", "rating": 900}
]

@app.get("/")
def root():
    return game_scores

@app.get("/scores")
def scores(limit: int = Query(5, ge=1, le=5)):
    return game_scores[:limit]

@app.get("/scores/{player_name}")
def get_score(player_name:str = Path(min_length=2)):
    for player in game_scores:
        if player["name"] == player_name:
            return player
    raise HTTPException(status_code=404, detail="Player not Found")

@app.put("/scores/{player_name}")
def update_score(
    data: Score_update,
    player_name:str = Path(min_length=2),
    ):
    for player in game_scores:
        if player["name"] == player_name:
            player["rating"] = data.rating
            return player
    raise HTTPException(status_code=404, detail="Player not found")
@app.post("/scores")
def create_score(score: Score):
    for player in game_scores:
        if player["name"] == score.name:
            raise HTTPException(status_code=409, detail="It already exists")
    game_scores.append(score.model_dump())
    return game_scores
@app.delete("/scores/{player_name}")
def delete_score(player_name:str = Path(min_length=2)):
    for player in game_scores:
        if player["name"] == player_name:
            game_scores.remove(player)
            return player
    raise HTTPException(status_code=404, detail="Player not Found")

##uvicorn main:app --reload
