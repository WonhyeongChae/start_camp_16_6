from types import SimpleNamespace

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
