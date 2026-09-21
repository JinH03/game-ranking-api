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

## Day 4 - 구조 분리 및 db 설치 및 이용

### 배운내용
- Router를 이용한 API 코드 분리
- schemas 폴더를 만들어 pydantic chema 분리
- main.py에서 router 연결
- API 기능별 파일 분리
- FASTAPI 프로젝트 구조 정리
- SQLAlchemy 설치 및 사용
- SQLite 데이터베이스 연결
- Database Engine 생성
- Session 구성
- SQLAlchemy Model 생성
- Dependency를 이용한 DB Session 관리
- 기존 메모리 리스트에서 데이터베이스 방식으로 변경
- CRUD API를 데이터베이스와 연결
  
### 프로젝트 구조

```text
game-ranking-api/
├── main.py
├── routers/
│   └── scores.py
├── schemas/
│   └── score.py
├── data/
│   └── scores.py
├── database.py
├── models.py
└── README.md
```

### 데이터베이스 구조

SQLite를 사용하여 `scores.db` 데이터베이스를 생성했다.

```text
FastAPI
   ↓
SQLAlchemy
   ↓
SQLite
   ↓
scores.db
```


## Day 5 - Request / Response Schema & response_model

### 배운내용
- Request Schema와 Response Schema의 차이
- Pydantic Response Schema 작성
- FastAPI `response_model` 사용
- SQLAlchemy Model과 Pydantic Schema의 역할 분리
- `from_attributes = True` 사용
- API 요청 데이터와 응답 데이터 분리


```text
Score
→ 내가 받는 데이터

Score_update
→ 수정할 때 받는 데이터

ScoreResponse
→ 내가 돌려주는 데이터

ScoreModel
→ DB에 저장되는 데이터
```
