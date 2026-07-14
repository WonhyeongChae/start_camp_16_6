먼저 다음 문서를 모두 읽어줘.

- ../docs/copilot-instructions.md
- ../docs/PROJECT_GUIDE.md
- ../docs/API_SPEC.md

나는 LocalHub 프로젝트의 BE 담당자다.

이번 작업의 목표는 backend 디렉터리에 FastAPI, SQLAlchemy, SQLite
기반 백엔드의 공통 구조를 만드는 것이다.

[기술 조건]
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- uvicorn
- 환경변수는 .env에서 읽음
- API prefix는 /api
- JSON 응답 필드는 camelCase
- OpenAI API 호출은 이후 백엔드에서만 구현

[이번 작업 범위]
1. 기존 backend 구조가 있으면 먼저 분석하고 유지한다.
2. 프로젝트가 없다면 최소 FastAPI 구조를 생성한다.
3. main.py에서 FastAPI 앱을 생성한다.
4. /api/health 엔드포인트를 구현한다.
5. SQLAlchemy와 SQLite 연결 구조를 만든다.
6. DB 세션 의존성 주입 구조를 만든다.
7. api, models, schemas, services 디렉터리를 역할별로 분리한다.
8. API_SPEC.md의 성공·실패 공통 응답 구조를 Pydantic 모델로 정의한다.
9. CORS_ORIGINS 환경변수를 이용해 CORS를 설정한다.
10. 전역 예외 처리의 기본 구조를 만든다.
11. 실행에 필요한 requirements.txt 또는 프로젝트 의존성 파일을 구성한다.
12. .env.example에 필요한 변수 이름만 제안한다.
13. 기본 health API 테스트를 작성한다.

[권장 구조]
backend/
├─ app/
│  ├─ main.py
│  ├─ api/
│  ├─ core/
│  ├─ db/
│  ├─ models/
│  ├─ schemas/
│  └─ services/
├─ tests/
└─ requirements.txt

기존 구조가 있다면 위 구조를 강제로 적용하지 말고 기존 구조를 우선한다.

[수정 가능 범위]
- backend/**
- 루트 .env.example은 기존 값과 충돌하지 않을 때만 수정

[금지 사항]
- frontend 파일 수정
- API_SPEC.md의 계약 변경
- 실제 OPENAI_API_KEY 작성
- CORS를 근거 없이 전체 허용
- 게시글·챗봇·추천 기능까지 한꺼번에 구현
- 불필요한 인증·회원 모델 추가
- 비밀번호 또는 환경변수 로그 출력

[완료 조건]
- uvicorn으로 서버 실행 가능
- GET /api/health가 공통 성공 응답을 반환
- SQLite 연결 구조가 준비됨
- 공통 응답·오류 모델이 존재함
- 테스트가 통과함
- Swagger 문서가 열림

작업 전 기존 구조와 구현 계획을 설명해줘.
작업 후에는 다음을 보고해줘.

1. 변경한 파일
2. 프로젝트 실행 방법
3. 테스트 명령어와 결과
4. 환경변수 목록
5. FE·데이터 담당자와 합의할 사항