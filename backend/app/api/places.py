from fastapi import APIRouter, Query

from app.schemas.common import SuccessEnvelope
from app.schemas.place import Place, PlaceListData
from app.services.places import get_place, list_places

router = APIRouter(prefix="/places", tags=["places"])


@router.get("", response_model=SuccessEnvelope[PlaceListData])
def read_places(page: int = Query(1, ge=1), size: int = Query(12, ge=1), type: str = "all",
                region: str = "all", keyword: str | None = None):
    data = list_places(page, size, type, region, keyword)
    return SuccessEnvelope[PlaceListData](data=data, message="장소 목록을 조회했습니다.")


@router.get("/{content_id}", response_model=SuccessEnvelope[Place])
def read_place(content_id: str):
    return SuccessEnvelope[Place](data=get_place(content_id), message="장소를 조회했습니다.")
