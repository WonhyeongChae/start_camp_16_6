# LocalHub Project Guide

> This guide exists to prevent three contributors and their Copilot sessions from producing incompatible code.

## 1. Fixed project scope

### Must have

- Gumi/Gyeongbuk provided JSON-based regional information service
- Anonymous community CRUD with password-based update/delete verification
- `POST /api/chat` and chat UI grounded in provided JSON and posts
- Vue.js 3 SPA, FastAPI, SQLAlchemy, SQLite
- Netlify FE deployment and Render BE deployment
- Code, DB, feature specification, data source/license notes, WBS, presentation materials

### Should have

- AI travel preference test and keyword-based place recommendations
- Festival calendar only when verified start/end dates are available

### Could have only after the above works

- Post search and view count
- Data visualization dashboard

### Won't have in this iteration

- Routing, weather, social sharing, realtime WebSocket notifications, multilingual content
- Account, login, or social authentication
- Expansion to unselected regions

Never add a new feature because it seems useful. Record it as a future idea instead.

## 2. Ownership

| Contributor | Primary ownership | Cooperation points |
|---|---|---|
| 원형 | FE: Vue structure, routing, regional/community/chat/test/calendar UI | Agree API shapes with 효정; result UI with 성식 |
| 효정 | BE: FastAPI, SQLite, CRUD, OpenAI server call, deployment | Agree data schemas with 성식; integration with 원형 |
| 성식 | AI/data: JSON normalization, derived tags, recommendation logic, festival data validation | Review AI grounding with 효정; result fields with 원형 |

Ownership is for coordination, not permission. Cross-cutting API, schema, environment, or deployment changes require review by another contributor.

## 3. Repository structure

```text
LocalHub/
├─ frontend/
├─ backend/
├─ data/
│  ├─ raw/              # supplied JSON; read-only
│  └─ derived/          # reviewed tags and verified supplemental fields
├─ docs/
│  ├─ API_SPEC.md
│  └─ PROJECT_GUIDE.md
├─ .github/
│  └─ copilot-instructions.md
├─ .env.example
├─ .gitignore
└─ README.md
```

Do not move folders or rename shared modules without team approval.

## 4. Git workflow

- `main`: deployable and reviewed only
- `develop`: integration branch
- Work in short-lived branches: `feature/fe-community`, `feature/be-post-api`, `feature/data-travel-tags`, `fix/chat-error`
- One task per branch and PR.
- Pull/rebase `develop` before starting and before requesting review.
- Never commit directly to `main`.
- Do not rewrite or delete another contributor's work to resolve a conflict; resolve together.
- Commit messages: `feat: ...`, `fix: ...`, `docs: ...`, `test: ...`, `refactor: ...`, `chore: ...`.

### Merge order

1. Base project and shared configuration
2. DB models and response envelope
3. JSON loader and normalization
4. Post/place APIs
5. FE routes and shared components
6. FE-BE integration
7. Chat
8. Travel test
9. Festival feature, if data permits
10. Deployment and stabilization

## 5. API and schema rules

- `docs/API_SPEC.md` is the source of truth.
- Never change paths, field names, enums, status codes, or response nesting locally without agreement.
- Backend defines request/response schemas explicitly with Pydantic.
- FE uses a centralized API client; do not scatter hard-coded base URLs.
- Add or update API tests before changing FE integration.
- Return the common envelope for both success and failure.
- Do not expose post passwords or OpenAI keys.

## 6. Data rules

- Treat all files under `data/raw/` as immutable source material.
- Public data license: show Korean Tourism Organization/TourAPI attribution and document the source/license.
- Store tags, normalized region names, verified dates, and other derived metadata in `data/derived/` keyed by `contentId`.
- Convert `mapx`/`mapy` to numbers only in application output; keep raw files unchanged.
- Do not infer missing facts. Empty source fields stay empty unless a verified derived source exists.
- The supplied festival list has no event start/end dates. `createdtime` and `modifiedtime` are metadata timestamps, not event dates.

## 7. AI and OpenAI rules

- Only the backend calls OpenAI. Never expose `OPENAI_API_KEY` in browser code.
- Recommendation type and ranking must be deterministic code, not an LLM decision.
- Use OpenAI for grounded chat phrasing and optional recommendation descriptions only.
- Retrieve relevant provided records/posts first; pass only those records as context.
- Instruct the model to say it lacks information when the context does not support an answer.
- Return references for grounded chat answers.
- Implement timeout, exception handling, and a deterministic fallback where applicable.
- Never let Copilot invent a package, endpoint, source field, secret, festival date, price, facility, or review.

## 8. Environment and security

`.env.example` may contain names, never real values:

```env
OPENAI_API_KEY=
DATABASE_URL=sqlite:///./localhub.db
CORS_ORIGINS=http://localhost:5173
VITE_API_BASE_URL=http://localhost:8000/api
```

- Add `.env`, local SQLite DB files, caches, and build outputs to `.gitignore` before the first commit.
- Do not print secrets or full passwords in logs.
- Validate post passwords on the server.
- Use explicit CORS origins; do not ship wildcard credentials configuration.

## 9. Copilot working procedure

Before asking Copilot to code:

1. Open `docs/API_SPEC.md`, `docs/PROJECT_GUIDE.md`, and the relevant existing files.
2. State the exact task, owned files, inputs/outputs, and acceptance checks.
3. Ask for a minimal change; forbid unrelated rewrites and new dependencies.
4. Ask Copilot to list assumptions before coding when the source is incomplete.

Recommended task prompt:

```text
Read .github/copilot-instructions.md, docs/PROJECT_GUIDE.md, and docs/API_SPEC.md first.
Task: [one concrete task]
Allowed files: [paths]
Acceptance criteria: [observable checks]
Do not add dependencies, rename shared fields, or edit unrelated files.
If the documents and code conflict, stop and report the conflict instead of guessing.
After editing, summarize changed files and provide the test command/result.
```

After Copilot edits:

1. Review every diff; do not accept blindly.
2. Check imports, field names, endpoints, error handling, and empty states.
3. Run the narrow test, then the relevant application test/build.
4. Remove debug output and fake data before PR.
5. Update documentation when an approved contract changes.

## 10. Definition of done

A task is done only when:

- It meets the WBS task and API contract.
- The app builds/runs locally.
- Relevant tests or manual verification pass.
- Loading, empty, success, and error cases are handled.
- No secret, password, debug log, or unrelated file is included.
- Another contributor can understand the PR description and reproduce the check.

## 11. Integration checkpoints

### Checkpoint 1: project skeleton

- FE and BE run independently.
- Shared environment names and API base URL are fixed.
- JSON loader returns the agreed `Place` shape.

### Checkpoint 2: required features

- Swagger verifies CRUD/place/chat contracts.
- FE replaces mocks with real endpoints.
- AI/data owner checks grounding and field accuracy.

### Checkpoint 3: selected features

- Travel test produces a deterministic type and top-three recommendations.
- Festival calendar is enabled only with verified dates.

### Checkpoint 4: release

- Netlify and Render URLs work together.
- CRUD, chat, travel test, and any enabled calendar flow pass end to end.
- Attribution, documentation, demo data, and presentation are ready.
- Freeze new features on 2026-07-15 evening; target final submission by 2026-07-16 14:30 KST.