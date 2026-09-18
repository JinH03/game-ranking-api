from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message":"hello World!"}

@app.get("/scores")
def scores():
    return [
        {"name":"Player1","rating":1500},
        {"name":"Player2","rating":1200},
        {"name":"Player3","rating":900}
    ]