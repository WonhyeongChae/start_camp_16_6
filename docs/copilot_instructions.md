# LocalHub Copilot Instructions

Read `PROJECT_GUIDE.md` and `API_SPEC.md` before proposing or editing code. They are authoritative.

## Mandatory behavior

- Stack is fixed: Vue.js 3 SPA, FastAPI, SQLAlchemy, SQLite.
- Make the smallest change required for the assigned task.
- Do not edit unrelated files, redesign architecture, rename shared fields, or add dependencies without explicit approval.
- Follow the exact API paths, request/response envelopes, field names, enums, and error codes in `docs/API_SPEC.md`.
- If code and documentation conflict, stop and explain the conflict. Do not guess.
- Preserve existing user/team changes and established style.
- Add validation, error handling, loading/empty states, and a relevant test or verification step.

## Data and AI safety

- Files under `data/raw/` are immutable.
- Store reviewed tags or verified supplemental fields under `data/derived/`, joined by `contentId`.
- Do not infer missing place facts or festival dates. `createdtime`/`modifiedtime` are not event dates.
- OpenAI calls are backend-only. Never expose keys in Vue or commit `.env`.
- Travel type and place ranking are deterministic code. OpenAI may phrase grounded explanations only.
- Ground chat answers in provided JSON/posts and return references. Never fabricate unsupported details.
- Never return or log post passwords.

## Before finishing a change

1. Review the diff for unrelated edits.
2. Verify API/schema compatibility.
3. Run the narrow test plus relevant build/run check.
4. Report changed files, assumptions, and test results.
5. Do not claim success when tests were not run or failed.