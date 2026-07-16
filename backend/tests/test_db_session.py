from types import SimpleNamespace

from sqlalchemy import inspect, text

from app.db.schema import ensure_runtime_schema
from app.db.session import create_db_engine, create_session_factory, get_db


class _DummyRequest:
    def __init__(self, session_factory) -> None:
        self.app = SimpleNamespace(state=SimpleNamespace(session_factory=session_factory))


def test_get_db_uses_app_state_session_factory() -> None:
    engine = create_db_engine("sqlite:///:memory:")
    session_factory = create_session_factory(engine)
    request = _DummyRequest(session_factory)

    db_generator = get_db(request)
    db = next(db_generator)

    assert db is not None
    assert db.is_active is True

    try:
        next(db_generator)
    except StopIteration:
        pass


def test_runtime_schema_adds_recommendation_count_to_existing_posts_table() -> None:
    engine = create_db_engine("sqlite:///:memory:")
    with engine.begin() as connection:
        connection.execute(text("CREATE TABLE posts (id INTEGER PRIMARY KEY)"))

    ensure_runtime_schema(engine)

    columns = {column["name"]: column for column in inspect(engine).get_columns("posts")}
    assert "recommendation_count" in columns
    assert columns["recommendation_count"]["nullable"] is False
