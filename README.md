# game-ranking-api

## Day 1 - FastAPI 기초
- 프로젝트 생성
- 파이썬 가상환경 생성 및 활성화
- fastapi와 uvicorn 설치
- GET '/' , '/scores' 엔드포인트 구현 및 swagger UI '/docs'를 이용해 api 테스트

### 오늘 핵심 개념
- FastAPI에서 배운 @app.get()을 이용해 URL과 파이썬 함수를 연결할 수 있다.
  ```@app.get("/score")
  def score():
  ```
- 위 코드는 /scores로 GET요청이 들어오면 scores() 함수를 실행한다.
