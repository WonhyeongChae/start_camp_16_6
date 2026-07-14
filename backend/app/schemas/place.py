from app.schemas.common import CamelModel


class Place(CamelModel):
    content_id: str
    content_type_id: str
    content_type: str
    title: str
    address: str
    detail_address: str
    telephone: str
    longitude: float | None
    latitude: float | None
    image_url: str
    thumbnail_url: str
    region: str
    tags: list[str]


class PlaceListData(CamelModel):
    items: list[Place]
    page: int
    size: int
    total: int
    total_pages: int
