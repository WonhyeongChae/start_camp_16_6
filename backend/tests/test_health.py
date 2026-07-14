from fastapi.testclient import TestClient

from app.main import create_app


def test_health_endpoint_returns_success_envelope() -> None:
    client = TestClient(create_app())

    response = client.get("/api/health")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] == "ok"
    assert body["message"] == "요청에 성공했습니다."
