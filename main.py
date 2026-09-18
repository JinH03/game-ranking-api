from fastapi import FastAPI
from fastapi import HTTPException, Query
app = FastAPI()

game_scores = [
    {"name": "Player1", "rating": 1500},
    {"name": "Player2", "rating": 1200},
    {"name": "Player3", "rating": 900}
]

@app.get("/")
def root():
    return game_scores

@app.get("/scores")
def scores(limit: int = Query(3, ge=1, le=3)):
    return game_scores[:limit]

@app.get("/scores/{player_name}")
def get_score(player_name):
    for player in game_scores():
        if player["name"] == player_name:
            return player
    raise HTTPException(status_code=404, detail="Player not Found")
##uvicorn main:app --reload
