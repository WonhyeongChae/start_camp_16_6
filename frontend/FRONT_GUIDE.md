먼저 다음 문서를 모두 읽어줘.

- ../docs/copilot-instructions.md
- ../docs/PROJECT_GUIDE.md
- ../docs/API_SPEC.md

나는 LocalHub 프로젝트의 FE 담당자다.

이번 작업의 목표는 frontend 디렉터리에 Vue.js 3 기반 프론트엔드의
공통 구조를 만드는 것이다.

[기술 조건]
- Vue.js 3
- Vite
- Vue Router
- JavaScript 사용
- SPA 구조
- API 주소는 VITE_API_BASE_URL 환경변수 사용
- OpenAI API를 프론트에서 직접 호출하지 않음
- 아직 UI 라이브러리는 추가하지 않음

[이번 작업 범위]
1. 기존 frontend 구조가 있으면 먼저 분석하고 유지한다.
2. 프로젝트가 없다면 Vue.js 3 + Vite 기반으로 구성한다.
3. 다음 라우트를 생성한다.
   - /
   - /places
   - /places/:contentId
   - /community
   - /community/write
   - /community/:id
   - /travel-test
   - /travel-result
   - /festivals
4. 공통 Header와 기본 Layout을 만든다.
5. 각 라우트에는 제목만 표시되는 최소 페이지를 만든다.
6. src/api/index.js에 공통 API 호출 모듈을 만든다.
7. API 모듈은 import.meta.env.VITE_API_BASE_URL을 사용한다.
8. 로딩, 빈 데이터, 오류 표시에 사용할 공통 컴포넌트 구조를 만든다.
9. .env 파일을 만들거나 실제 URL·키를 하드코딩하지 않는다.
10. 필요한 환경변수 이름만 .env.example에 제안한다.

[수정 가능 범위]
- frontend/**
- 루트 .env.example은 기존 내용과 충돌하지 않을 때만 수정

[금지 사항]
- 백엔드 파일 수정
- API_SPEC.md의 경로 또는 필드명 변경
- 실제 API가 완성됐다고 가정
- 임의의 UI 라이브러리 추가
- 지역 정보·게시글 화면의 세부 기능까지 한꺼번에 구현
- 관련 없는 파일 전체 재작성

[완료 조건]
- npm install 후 실행 가능
- 각 URL로 이동 가능
- Header를 통해 주요 페이지 이동 가능
- API base URL이 환경변수로 분리됨
- 빌드 오류가 없음

작업 전 기존 파일 구조와 구현 계획을 간단히 설명해줘.
작업 후에는 다음을 보고해줘.

1. 변경한 파일
2. 구현한 라우트
3. 추가한 의존성
4. 실행한 명령어와 결과
5. BE·데이터 담당자와 합의가 필요한 사항