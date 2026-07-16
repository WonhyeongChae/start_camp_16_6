from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine


def ensure_runtime_schema(engine: Engine) -> None:
    """create_all로 갱신되지 않는 기존 SQLite 테이블의 신규 컬럼을 보완합니다."""
    inspector = inspect(engine)
    if "posts" not in inspector.get_table_names():
        return

    column_names = {column["name"] for column in inspector.get_columns("posts")}
    if "recommendation_count" not in column_names:
        with engine.begin() as connection:
            connection.execute(
                text(
                    "ALTER TABLE posts "
                    "ADD COLUMN recommendation_count INTEGER NOT NULL DEFAULT 0"
                )
            )
