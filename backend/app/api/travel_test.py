from fastapi import APIRouter

from app.schemas.common import SuccessEnvelope
from app.schemas.travel_test import TravelTestData, TravelTestRequest
from app.services.travel_test import analyze_travel_test

router = APIRouter(prefix="/travel-test", tags=["travel-test"])


@router.post("", response_model=SuccessEnvelope[TravelTestData])
def submit_travel_test(payload: TravelTestRequest):
    return SuccessEnvelope[TravelTestData](data=analyze_travel_test(payload), message="여행 취향 분석을 완료했습니다.")
