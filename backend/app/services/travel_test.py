import json
from pathlib import Path

from fastapi import HTTPException

from app.schemas.travel_test import Recommendation, TravelTestData, TravelTestRequest, TravelType
from data.travel_recommender import load_travel_types, recommend_places


QUESTION_FILE = Path(__file__).resolve().parents[3] / "data" / "derived" / "travel_test_questions.json"
DESCRIPTIONS = {
    "HEALING": "복잡한 일정보다 자연 속에서 천천히 머무는 여행을 선호하는 유형입니다.",
    "EXPLORER": "새로운 체험과 야외 활동을 적극적으로 즐기는 여행 유형입니다.",
    "CULTURE": "장소의 역사와 문화, 감성적인 볼거리를 즐기는 여행 유형입니다.",
    "FOODIE": "지역의 음식과 시장, 특색 있는 먹거리를 찾아다니는 여행 유형입니다.",
}


def analyze_travel_test(payload: TravelTestRequest) -> TravelTestData:
    config = json.loads(QUESTION_FILE.read_text(encoding="utf-8"))
    questions = {item["questionId"]: item for item in config["questions"]}
    answers = payload.answers
    if len(answers) != config["requiredAnswerCount"] or len({answer.question_id for answer in answers}) != len(answers):
        raise HTTPException(status_code=400, detail="모든 질문에 한 번씩 답해야 합니다.")

    scores = {code: 0 for code in config["validTypeCodes"]}
    primary_by_question: dict[int, str] = {}
    for answer in answers:
        question = questions.get(answer.question_id)
        option = next((item for item in question.get("options", []) if item["optionId"] == answer.option_id), None) if question else None
        if option is None:
            raise HTTPException(status_code=400, detail="질문 또는 선택지 ID가 올바르지 않습니다.")
        primary_by_question[answer.question_id] = option["primaryType"]
        for code, value in option["scores"].items():
            scores[code] += value

    maximum = max(scores.values())
    tied = [code for code, value in scores.items() if value == maximum]
    selected = next((primary_by_question[qid] for qid in config["tieBreakQuestionOrder"] if primary_by_question[qid] in tied), None)
    if selected is None:
        selected = next(code for code in config["fallbackTypeOrder"] if code in tied)

    type_config = load_travel_types()[selected]
    recommendations = [Recommendation.model_validate(item) for item in recommend_places(selected, limit=3)]
    travel_type = TravelType(code=selected, name=type_config["name"], description=DESCRIPTIONS[selected], keywords=type_config["keywords"])
    return TravelTestData(travel_type=travel_type, recommendations=recommendations)
