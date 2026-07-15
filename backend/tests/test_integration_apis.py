from pathlib import Path
import sys

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.main import create_app


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


def test_chat_uses_place_and_post_references() -> None:
    with TestClient(create_app()) as client:
        place = client.get("/api/places", params={"region": "구미", "size": 1}).json()["data"]["items"][0]
        response = client.post("/api/chat", json={"message": f"{place['title']} 정보를 알려줘", "history": []})
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["answer"]
        assert any(ref["type"] == "place" and ref["id"] == place["contentId"] for ref in data["references"])


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
