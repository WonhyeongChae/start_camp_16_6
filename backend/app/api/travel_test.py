from fastapi import APIRouter

from app.schemas.common import SuccessEnvelope
from app.schemas.travel_test import TravelTestData, TravelTestQuestionsData, TravelTestRequest
from app.services.travel_test import analyze_travel_test, get_travel_test_questions

router = APIRouter(prefix="/travel-test", tags=["travel-test"])


@router.get("/questions", response_model=SuccessEnvelope[TravelTestQuestionsData])
def read_travel_test_questions():
    return SuccessEnvelope[TravelTestQuestionsData](
        data=get_travel_test_questions(),
        message="여행 취향 질문을 조회했습니다.",
    )


@router.post("", response_model=SuccessEnvelope[TravelTestData])
def submit_travel_test(payload: TravelTestRequest):
    return SuccessEnvelope[TravelTestData](data=analyze_travel_test(payload), message="여행 취향 분석을 완료했습니다.")
