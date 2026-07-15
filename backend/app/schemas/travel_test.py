from pydantic import Field

from app.schemas.common import CamelModel


class TravelAnswer(CamelModel):
    question_id: int
    option_id: str = Field(min_length=1)


class TravelTestRequest(CamelModel):
    answers: list[TravelAnswer]


class TravelTestOption(CamelModel):
    option_id: str
    text: str


class TravelTestQuestion(CamelModel):
    question_id: int
    question: str
    options: list[TravelTestOption]


class TravelTestQuestionsData(CamelModel):
    version: str
    required_answer_count: int
    questions: list[TravelTestQuestion]


class TravelType(CamelModel):
    code: str
    name: str
    description: str
    keywords: list[str]


class Recommendation(CamelModel):
    content_id: str
    title: str
    content_type: str
    address: str
    image_url: str
    matched_keywords: list[str]
    match_score: int
    reason: str


class TravelTestData(CamelModel):
    travel_type: TravelType
    recommendations: list[Recommendation]
