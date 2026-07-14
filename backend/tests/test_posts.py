from fastapi.testclient import TestClient

from app.main import create_app


def _create_post(client: TestClient, title: str, content: str, category: str = "여행", nickname: str = "익명", password: str = "1234"):
    response = client.post(
        "/api/posts",
        json={
            "title": title,
            "content": content,
            "category": category,
            "nickname": nickname,
            "password": password,
        },
    )
    assert response.status_code == 201
    return response.json()["data"]


def test_create_post_returns_expected_shape_and_excludes_password() -> None:
    with TestClient(create_app()) as client:
        data = _create_post(client, "구미 여행지 추천 부탁드립니다", "주말에 가볼 만한 장소가 있을까요?")

        assert data["title"] == "구미 여행지 추천 부탁드립니다"
        assert data["content"] == "주말에 가볼 만한 장소가 있을까요?"
        assert data["category"] == "여행"
        assert data["nickname"] == "익명"
        assert "password" not in data
        assert "viewCount" in data
        assert "createdAt" in data
        assert "updatedAt" in data


def test_detail_increments_view_count() -> None:
    with TestClient(create_app()) as client:
        data = _create_post(client, "조회수 테스트", "본문")
        post_id = data["id"]

        first = client.get(f"/api/posts/{post_id}")
        second = client.get(f"/api/posts/{post_id}")

        assert first.status_code == 200
        assert second.status_code == 200
        assert first.json()["data"]["viewCount"] == 1
        assert second.json()["data"]["viewCount"] == 2


def test_list_posts_supports_keyword_category_sort_and_pagination() -> None:
    with TestClient(create_app()) as client:
        _create_post(client, "첫 번째 글", "구미 산책 장소", category="여행")
        _create_post(client, "두 번째 글", "맛집 후기", category="맛집")
        _create_post(client, "세 번째 글", "구미 맛집 추천", category="맛집")

        keyword_response = client.get("/api/posts", params={"keyword": "구미"})
        assert keyword_response.status_code == 200
        keyword_items = keyword_response.json()["data"]["items"]
        assert len(keyword_items) >= 2
        assert all("구미" in item["title"] or "구미" in item["content"] for item in keyword_items)

        category_response = client.get("/api/posts", params={"category": "맛집"})
        assert category_response.status_code == 200
        category_items = category_response.json()["data"]["items"]
        assert category_items
        assert all(item["category"] == "맛집" for item in category_items)

        client.get("/api/posts/1")
        client.get("/api/posts/1")
        views_response = client.get("/api/posts", params={"sort": "views"})
        assert views_response.status_code == 200
        views_items = views_response.json()["data"]["items"]
        assert views_items

        page_response = client.get("/api/posts", params={"page": 1, "size": 2})
        assert page_response.status_code == 200
        page_data = page_response.json()["data"]
        assert page_data["page"] == 1
        assert page_data["size"] == 2
        assert page_data["total"] >= 3
        assert len(page_data["items"]) <= 2


def test_update_post_password_mismatch_returns_403_invalid_password() -> None:
    with TestClient(create_app()) as client:
        data = _create_post(client, "테스트 글", "본문")
        post_id = data["id"]

        update_response = client.put(
            f"/api/posts/{post_id}",
            json={
                "title": "수정",
                "content": "수정 본문",
                "category": "자유",
                "nickname": "익명",
                "password": "wrong",
            },
        )

        assert update_response.status_code == 403
        body = update_response.json()
        assert body["error"]["code"] == "INVALID_PASSWORD"


def test_update_post_success() -> None:
    with TestClient(create_app()) as client:
        data = _create_post(client, "수정 전", "수정 전 본문", category="자유")
        post_id = data["id"]

        update_response = client.put(
            f"/api/posts/{post_id}",
            json={
                "title": "수정 후",
                "content": "수정 후 본문",
                "category": "생활",
                "nickname": "익명",
                "password": "1234",
            },
        )

        assert update_response.status_code == 200
        body = update_response.json()["data"]
        assert body["title"] == "수정 후"
        assert body["content"] == "수정 후 본문"
        assert body["category"] == "생활"
        assert "password" not in body


def test_delete_post_password_mismatch_returns_403_invalid_password() -> None:
    with TestClient(create_app()) as client:
        data = _create_post(client, "삭제 테스트", "본문")
        post_id = data["id"]

        delete_response = client.request(
            "DELETE",
            f"/api/posts/{post_id}",
            json={"password": "wrong"},
        )

        assert delete_response.status_code == 403
        assert delete_response.json()["error"]["code"] == "INVALID_PASSWORD"


def test_delete_post_success() -> None:
    with TestClient(create_app()) as client:
        data = _create_post(client, "삭제 성공", "본문")
        post_id = data["id"]

        delete_response = client.request(
            "DELETE",
            f"/api/posts/{post_id}",
            json={"password": "1234"},
        )

        assert delete_response.status_code == 200
        assert delete_response.json()["data"]["id"] == post_id

        detail_response = client.get(f"/api/posts/{post_id}")
        assert detail_response.status_code == 404


def test_list_posts_invalid_query_returns_400() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/api/posts", params={"sort": "invalid"})
        assert response.status_code == 400
        assert response.json()["error"]["code"] == "INVALID_REQUEST"