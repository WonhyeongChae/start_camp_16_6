from math import ceil

from fastapi import HTTPException

from app.schemas.place import Place, PlaceListData
from data.place_loader import ALLOWED_REGIONS, CONTENT_TYPE_MAP, filter_places, get_place_by_id, load_place_dataset


def _load_places() -> list[dict]:
    try:
        return load_place_dataset()
    except (OSError, ValueError) as exc:
        raise HTTPException(status_code=500, detail="장소 데이터를 불러올 수 없습니다.") from exc


def list_places(page: int, size: int, content_type: str | None, region: str | None, keyword: str | None) -> PlaceListData:
    if content_type not in (None, "", "all") and content_type not in CONTENT_TYPE_MAP:
        raise HTTPException(status_code=400, detail="장소 유형이 올바르지 않습니다.")
    if region not in (None, "", "all") and region not in ALLOWED_REGIONS:
        raise HTTPException(status_code=400, detail="지역이 올바르지 않습니다.")
    places = filter_places(
        _load_places(),
        content_type=None if content_type in (None, "", "all") else content_type,
        region=None if region in (None, "", "all") else region,
        keyword=keyword,
    )
    total = len(places)
    start = (page - 1) * size
    return PlaceListData(items=[Place.model_validate(item) for item in places[start:start + size]], page=page, size=size,
                         total=total, total_pages=ceil(total / size) if total else 0)


def get_place(content_id: str) -> Place:
    place = get_place_by_id(_load_places(), content_id)
    if place is None:
        raise HTTPException(status_code=404, detail="장소를 찾을 수 없습니다.")
    return Place.model_validate(place)
