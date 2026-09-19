# game-ranking-api

## Day 1 - FastAPI 기초
- 프로젝트 생성
- 파이썬 가상환경 생성 및 활성화
- fastapi와 uvicorn 설치
- GET '/' , '/scores' 엔드포인트 구현 및 swagger UI '/docs'를 이용해 api 테스트

### 오늘 핵심 개념
- FastAPI에서 배운 @app.get()을 이용해 URL과 파이썬 함수를 연결할 수 있다.
  ```
  @app.get("/score")
  def score():
    return .....
  ```
- 위 코드는 /scores로 GET요청이 들어오면 scores() 함수를 실행한다.


## Day 2 - 패스 파라미터 & 쿼리 파라미터
- path, Query Parameter 학습
- 특정 플레이어 조회 API 구현
- 존재하지 않는 플레이어에 대한 404 에러 처리
- HttpException을 이용한 404처리
- HTTP 422 응답 확인 game-ranking-api
```
@app.get("/scores/{player_name}")
def get_score(player_name):
    for player in game_scores:
        if player["name"] == player_name:
            return player
    raise HTTPException(status_code=404, detail="Player not Found")
```

## Day 3 - CRUD & 데이터 검증

### 배운내용

- Pydantic 'BaseModel' 사용
- Field()로 입력값 검증
- Query()로 쿼리 파라미터 검증
- path()를 통한 URL 파라미터 검증
- CRUD API 구현

### 구현 API
  
- `GET /scores` → 전체 점수 조회
- `GET /scores/{player_name}` → 특정 플레이어 조회
- `POST /scores` → 플레이어 추가
- `PUT /scores/{player_name}` → 점수 수정
- `DELETE /scores/{player_name}` → 플레이어 삭제

### 검증 조건
- 이름은 최소 2글자
- rating은 0 이상
- limit은 1~5
- 존재하지 않는 플레이어 → 404
- 중복 플레이어 → 409
- 잘못된 입력 → 422
