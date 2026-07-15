import json
from pathlib import Path

from fastapi import HTTPException

from app.schemas.travel_test import (
    Recommendation,
    TravelTestData,
    TravelTestOption,
    TravelTestQuestion,
    TravelTestQuestionsData,
    TravelTestRequest,
    TravelType,
)
from data.travel_recommender import load_travel_types, recommend_places


QUESTION_FILE = Path(__file__).resolve().parents[3] / "data" / "derived" / "travel_test_questions.json"


def _load_question_config() -> dict:
    try:
        config = json.loads(QUESTION_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=500, detail="여행 취향 질문 데이터를 불러올 수 없습니다.") from exc

    if not isinstance(config, dict) or not isinstance(config.get("questions"), list):
        raise HTTPException(status_code=500, detail="여행 취향 질문 데이터 구조가 올바르지 않습니다.")
    return config


def get_travel_test_questions() -> TravelTestQuestionsData:
    config = _load_question_config()
    try:
        questions = [
            TravelTestQuestion(
                question_id=question["questionId"],
                question=question["question"],
                options=[
                    TravelTestOption(option_id=option["optionId"], text=option["text"])
                    for option in question["options"]
                ],
            )
            for question in config["questions"]
        ]
        return TravelTestQuestionsData(
            version=str(config["version"]),
            required_answer_count=config["requiredAnswerCount"],
            questions=questions,
        )
    except (KeyError, TypeError) as exc:
        raise HTTPException(status_code=500, detail="여행 취향 질문 데이터 구조가 올바르지 않습니다.") from exc


def analyze_travel_test(payload: TravelTestRequest) -> TravelTestData:
    config = _load_question_config()
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
    travel_type = TravelType(
        code=selected,
        name=type_config["name"],
        description=type_config["description"],
        keywords=type_config["keywords"],
    )
    return TravelTestData(travel_type=travel_type, recommendations=recommendations)
