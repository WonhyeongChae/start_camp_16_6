from fastapi import APIRouter

from app.schemas.common import HealthData, SuccessEnvelope

router = APIRouter(tags=["health"])


@router.get("/health", response_model=SuccessEnvelope[HealthData])
def health_check() -> SuccessEnvelope[HealthData]:
    return SuccessEnvelope[HealthData](data=HealthData(status="ok"))
