from datetime import date
from pathlib import Path
import sys

from fastapi.testclient import TestClient
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.main import create_app
from app.core.config import load_settings
from app.services import chat as chat_service


def test_travel_test_questions_hide_scoring_metadata() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/api/travel-test/questions")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["version"] == "1.0"
    assert data["requiredAnswerCount"] == 5
    assert len(data["questions"]) == 5
    option = data["questions"][0]["options"][0]
    assert set(option) == {"optionId", "text"}
    assert "scores" not in response.text
    assert "primaryType" not in response.text


def test_places_list_detail_and_not_found() -> None:
    with TestClient(create_app()) as client:
        listing = client.get("/api/places", params={"page": 1, "size": 2, "region": "구미"})
        assert listing.status_code == 200
        body = listing.json()["data"]
        assert len(body["items"]) <= 2
        assert body["totalPages"] >= 1
        place = body["items"][0]
        detail = client.get(f"/api/places/{place['contentId']}")
        assert detail.status_code == 200
        assert detail.json()["data"] == place
        assert client.get("/api/places/not-found").status_code == 404


def test_chat_calls_gpt_5_mini_with_place_references(monkeypatch) -> None:
    captured: dict[str, object] = {}

    class FakeResponses:
        def create(self, **kwargs):
            captured.update(kwargs)
            return SimpleNamespace(
                output_text="모델이 생성한 여행 답변",
                status="completed",
                incomplete_details=None,
                usage=SimpleNamespace(
                    output_tokens=20,
                    output_tokens_details=SimpleNamespace(reasoning_tokens=5),
                ),
            )

    class FakeOpenAI:
        def __init__(self, api_key: str):
            captured["api_key"] = api_key
            self.responses = FakeResponses()

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-5-mini")
    monkeypatch.setattr(chat_service, "OpenAI", FakeOpenAI)
    load_settings.cache_clear()

    try:
        with TestClient(create_app()) as client:
            place = client.get("/api/places", params={"region": "구미", "size": 1}).json()["data"]["items"][0]
            response = client.post(
                "/api/chat",
                json={
                    "message": f"{place['title']} 정보를 알려줘",
                    "history": [{"role": "user", "content": "가족 여행이야"}],
                },
            )

        assert response.status_code == 200
        data = response.json()["data"]
        assert data["answer"] == "모델이 생성한 여행 답변"
        assert any(ref["type"] == "place" and ref["id"] == place["contentId"] for ref in data["references"])
        assert captured["model"] == "gpt-5-mini"
        assert captured["reasoning"] == {"effort": "minimal"}
        assert captured["max_output_tokens"] == 3000
        assert captured["input"][0] == {"role": "user", "content": "가족 여행이야"}
        assert "참고 정보:" in captured["input"][-1]["content"]
    finally:
        load_settings.cache_clear()


def test_chat_finds_july_gumi_festivals_from_natural_language(monkeypatch) -> None:
    captured: dict[str, object] = {}

    class FakeResponses:
        def create(self, **kwargs):
            captured.update(kwargs)
            return SimpleNamespace(
                output_text="7월 구미 축제 안내",
                status="completed",
                incomplete_details=None,
                usage=SimpleNamespace(
                    output_tokens=20,
                    output_tokens_details=SimpleNamespace(reasoning_tokens=5),
                ),
            )

    class FakeOpenAI:
        def __init__(self, api_key: str):
            self.responses = FakeResponses()

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(chat_service, "OpenAI", FakeOpenAI)
    load_settings.cache_clear()

    try:
        with TestClient(create_app()) as client:
            expected = client.get(
                "/api/festivals",
                params={"year": 2026, "month": 7},
            ).json()["data"]
            response = client.post(
                "/api/chat",
                json={"message": "7월에 있는 구미의 축제 몇 가지 알려줘", "history": []},
            )

        assert response.status_code == 200
        references = response.json()["data"]["references"]
        festival_ids = {item["id"] for item in references if item["type"] == "festival"}
        assert festival_ids == {item["contentId"] for item in expected[:5]}
        context = captured["input"][-1]["content"]
        assert "정확히 일치하는 축제 없음: 지역=구미, 월=7" in context
        assert "festival:" in context
        assert all(item["title"] in context for item in expected[:5])
    finally:
        load_settings.cache_clear()


def test_chat_finds_nearest_upcoming_festival_from_today(monkeypatch) -> None:
    captured: dict[str, object] = {}

    class FakeResponses:
        def create(self, **kwargs):
            captured.update(kwargs)
            return SimpleNamespace(
                output_text="가장 가까운 축제 안내",
                status="completed",
                incomplete_details=None,
                usage=SimpleNamespace(
                    output_tokens=20,
                    output_tokens_details=SimpleNamespace(reasoning_tokens=5),
                ),
            )

    class FakeOpenAI:
        def __init__(self, api_key: str):
            self.responses = FakeResponses()

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(chat_service, "OpenAI", FakeOpenAI)
    monkeypatch.setattr(chat_service, "_today", lambda: date(2026, 7, 15))
    load_settings.cache_clear()

    try:
        with TestClient(create_app()) as client:
            festivals = client.get("/api/festivals").json()["data"]
            expected = min(
                (item for item in festivals if item["endDate"] >= "2026-07-15"),
                key=lambda item: (max(item["startDate"], "2026-07-15"), item["endDate"], item["contentId"]),
            )
            response = client.post(
                "/api/chat",
                json={
                    "message": "지금 날짜 기준으로 가장 가까운 시일 내에 있는 축제 하나를 추천해줘",
                    "history": [],
                },
            )

        assert response.status_code == 200
        festival_references = [
            item for item in response.json()["data"]["references"]
            if item["type"] == "festival"
        ]
        assert festival_references == [{
            "type": "festival",
            "id": expected["contentId"],
            "title": expected["title"],
        }]
        context = captured["input"][-1]["content"]
        assert "기준일=2026-07-15" in context
        assert expected["startDate"] in context
        assert expected["endDate"] in context
    finally:
        load_settings.cache_clear()


def test_chat_connects_all_community_example_questions_to_posts(monkeypatch) -> None:
    captured_contexts: list[str] = []

    class FakeResponses:
        def create(self, **kwargs):
            captured_contexts.append(kwargs["input"][-1]["content"])
            return SimpleNamespace(
                output_text="커뮤니티 게시글을 바탕으로 답변했습니다.",
                status="completed",
                incomplete_details=None,
                usage=SimpleNamespace(
                    output_tokens=20,
                    output_tokens_details=SimpleNamespace(reasoning_tokens=5),
                ),
            )

    class FakeOpenAI:
        def __init__(self, api_key: str):
            self.responses = FakeResponses()

    seed_posts = [
        ("구미 대표 여행지 추천", "금오산과 금오천을 구미 여행지로 추천합니다.", "여행"),
        ("금오산 등산 후기", "금오산에 직접 다녀온 등산 경험과 정상 풍경 후기입니다.", "여행"),
        ("새마을시장 구미 맛집", "구미 새마을시장에서 먹은 지역 음식과 맛집 후기입니다.", "맛집"),
        ("아이와 함께하는 낙동강 체험", "어린이와 가족이 함께 가기 좋은 체험 장소입니다.", "여행"),
        ("금오천 연인 데이트 코스", "커플이 걷기 좋은 금오천 데이트 코스를 소개합니다.", "여행"),
        ("주말 동락공원 나들이", "주말에 가볼 만한 동락공원 나들이 장소입니다.", "여행"),
        ("구미 라면축제 방문 후기", "구미 라면축제 행사와 먹거리 체험을 요약한 글입니다.", "축제"),
        ("선산시장 지역 음식 이야기", "선산시장 먹거리와 구미 지역 음식을 소개합니다.", "맛집"),
        ("금오천 산책 장소 추천", "커뮤니티 이용자가 추천한 조용한 산책 장소입니다.", "여행"),
        ("최근 금오산 여행 후기", "최근 작성한 금오산 여행 경험과 방문 후기입니다.", "여행"),
    ]
    cases = [
        ("커뮤니티에서 추천한 구미 여행지는 어디야?", "구미 대표 여행지 추천"),
        ("금오산에 다녀온 사람들의 후기가 있어?", "금오산 등산 후기"),
        ("구미 맛집과 관련된 게시글을 찾아줘.", "새마을시장 구미 맛집"),
        ("아이와 함께 가기 좋은 장소를 추천한 글이 있어?", "아이와 함께하는 낙동강 체험"),
        ("데이트 코스로 추천한 장소가 있는지 알려줘.", "금오천 연인 데이트 코스"),
        ("주말에 가볼 만한 곳을 소개한 게시글을 찾아줘.", "주말 동락공원 나들이"),
        ("구미 축제에 관한 커뮤니티 글을 요약해 줘.", "구미 라면축제 방문 후기"),
        ("최근 작성된 여행 후기에는 어떤 내용이 있어?", "최근 금오산 여행 후기"),
        ("시장이나 지역 음식과 관련된 게시글이 있어?", "선산시장 지역 음식 이야기"),
        ("커뮤니티 이용자들이 추천한 산책 장소를 알려줘.", "금오천 산책 장소 추천"),
    ]

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(chat_service, "OpenAI", FakeOpenAI)
    load_settings.cache_clear()

    try:
        with TestClient(create_app()) as client:
            created: dict[str, int] = {}
            for title, content, category in seed_posts:
                response = client.post("/api/posts", json={
                    "title": title,
                    "content": content,
                    "category": category,
                    "nickname": "테스터",
                    "password": "1234",
                })
                assert response.status_code == 201
                created[title] = response.json()["data"]["id"]

            for _ in range(5):
                recommend_response = client.post(
                    f"/api/posts/{created['구미 대표 여행지 추천']}/recommend"
                )
                assert recommend_response.status_code == 200

            for index, (question, expected_title) in enumerate(cases):
                response = client.post("/api/chat", json={"message": question, "history": []})
                assert response.status_code == 200
                data = response.json()["data"]
                post_references = [item for item in data["references"] if item["type"] == "post"]
                assert post_references, question
                assert any(item["title"] == expected_title for item in post_references), question
                assert expected_title in captured_contexts[index], question
                assert "recommendations=" in captured_contexts[index], question
                assert "created=" in captured_contexts[index], question
    finally:
        load_settings.cache_clear()


def test_chat_returns_openai_api_error_without_api_key(monkeypatch) -> None:
    # 로컬 .env가 있어도 빈 프로세스 환경변수가 우선하도록 테스트를 격리합니다.
    monkeypatch.setenv("OPENAI_API_KEY", "")
    load_settings.cache_clear()

    try:
        with TestClient(create_app(), raise_server_exceptions=False) as client:
            response = client.post("/api/chat", json={"message": "여행지를 추천해줘", "history": []})

        assert response.status_code == 500
        assert response.json()["error"]["code"] == "OPENAI_API_ERROR"
    finally:
        load_settings.cache_clear()


def test_chat_reports_output_token_exhaustion(monkeypatch) -> None:
    class FakeResponses:
        def create(self, **kwargs):
            return SimpleNamespace(
                output_text="",
                status="incomplete",
                incomplete_details=SimpleNamespace(reason="max_output_tokens"),
                usage=SimpleNamespace(
                    output_tokens=3000,
                    output_tokens_details=SimpleNamespace(reasoning_tokens=3000),
                ),
            )

    class FakeOpenAI:
        def __init__(self, api_key: str):
            assert api_key == "test-key"
            self.responses = FakeResponses()

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(chat_service, "OpenAI", FakeOpenAI)
    load_settings.cache_clear()

    try:
        with TestClient(create_app(), raise_server_exceptions=False) as client:
            response = client.post("/api/chat", json={"message": "가족 축제를 추천해줘", "history": []})

        assert response.status_code == 500
        assert response.json()["error"] == {
            "code": "OPENAI_API_ERROR",
            "detail": "OpenAI 응답 생성 토큰이 부족합니다.",
        }
    finally:
        load_settings.cache_clear()


def test_travel_test_returns_type_and_recommendations() -> None:
    payload = {"answers": [
        {"questionId": 1, "optionId": "Q1_A"}, {"questionId": 2, "optionId": "Q2_C"},
        {"questionId": 3, "optionId": "Q3_A"}, {"questionId": 4, "optionId": "Q4_B"},
        {"questionId": 5, "optionId": "Q5_D"},
    ]}
    with TestClient(create_app()) as client:
        response = client.post("/api/travel-test", json=payload)
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["travelType"]["code"] == "HEALING"
        assert data["travelType"]["description"]
        assert len(data["recommendations"]) <= 3
        assert all("matchScore" in item for item in data["recommendations"])


def test_travel_test_rejects_duplicate_question() -> None:
    payload = {"answers": [{"questionId": 1, "optionId": "Q1_A"}] * 5}
    with TestClient(create_app()) as client:
        response = client.post("/api/travel-test", json=payload)
        assert response.status_code == 400
        assert response.json()["error"]["code"] == "INVALID_REQUEST"
