from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict


def to_camel(value: str) -> str:
    parts = value.split("_")
    return parts[0] + "".join(part.capitalize() for part in parts[1:])


class CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class HealthData(CamelModel):
    status: str


class ErrorDetail(CamelModel):
    code: str
    detail: str


T = TypeVar("T")


class SuccessEnvelope(CamelModel, Generic[T]):
    success: bool = True
    data: T
    message: str = "요청에 성공했습니다."


class PaginatedData(CamelModel, Generic[T]):
    items: list[T]
    page: int
    size: int
    total: int
    total_pages: int


class PaginatedSuccessEnvelope(SuccessEnvelope[PaginatedData[T]], Generic[T]):
    message: str = "목록을 조회했습니다."


class ErrorEnvelope(CamelModel):
    success: bool = False
    data: None = None
    message: str = "요청을 처리할 수 없습니다."
    error: ErrorDetail
