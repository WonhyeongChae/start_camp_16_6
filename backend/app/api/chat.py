from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.chat import ChatData, ChatRequest
from app.schemas.common import SuccessEnvelope
from app.services.chat import create_grounded_answer

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=SuccessEnvelope[ChatData])
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    return SuccessEnvelope[ChatData](data=create_grounded_answer(db, payload), message="챗봇 답변을 생성했습니다.")
