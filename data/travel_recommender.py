from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from data.place_loader import get_place_by_id, load_place_dataset

BASE_DIR = Path(__file__).resolve().parent
DERIVED_DIR = BASE_DIR / "derived"
VALID_TRAVEL_TYPES = {"HEALING", "EXPLORER", "CULTURE", "FOODIE"}


def load_travel_types() -> Dict[str, Dict[str, Any]]:
    path = DERIVED_DIR / "travel_types.json"
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, dict):
        raise ValueError("travel_types.json 구조가 올바르지 않습니다.")
    if set(data) != VALID_TRAVEL_TYPES:
        raise ValueError("travel_types.json의 여행 유형 코드가 올바르지 않습니다.")

    result: Dict[str, Dict[str, Any]] = {}
    for travel_type, config in data.items():
        if not isinstance(config, dict):
            raise ValueError(f"travel_types.json의 {travel_type} 설정이 올바르지 않습니다.")
        name = config.get("name")
        description = config.get("description")
        keywords = config.get("keywords")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"travel_types.json의 {travel_type} 이름이 올바르지 않습니다.")
        if not isinstance(description, str) or not description.strip():
            raise ValueError(f"travel_types.json의 {travel_type} 설명이 올바르지 않습니다.")
        if not isinstance(keywords, list) or not all(isinstance(keyword, str) for keyword in keywords):
            raise ValueError(f"travel_types.json의 {travel_type} 키워드가 올바르지 않습니다.")
        result[str(travel_type)] = {
            "name": name,
            "description": description,
            "keywords": keywords,
        }
    return result


def load_travel_candidates() -> Dict[str, Dict[str, Any]]:
    path = DERIVED_DIR / "travel_candidates.json"
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, dict):
        raise ValueError("travel_candidates.json 구조가 올바르지 않습니다.")

    result: Dict[str, Dict[str, Any]] = {}
    for content_id, config in data.items():
        if not isinstance(config, dict):
            raise ValueError(f"travel_candidates.json의 {content_id} 설정이 올바르지 않습니다.")
        recommended_types = config.get("recommendedTypes")
        review_required = config.get("reviewRequired")
        if not isinstance(recommended_types, list) or not all(isinstance(item, str) for item in recommended_types):
            raise ValueError(f"travel_candidates.json의 {content_id} recommendedTypes가 올바르지 않습니다.")
        if not isinstance(review_required, bool):
            raise ValueError(f"travel_candidates.json의 {content_id} reviewRequired가 올바르지 않습니다.")
        result[str(content_id)] = {
            "recommendedTypes": recommended_types,
            "reviewRequired": review_required,
        }
    return result


def recommend_places(travel_type_code: str, limit: int = 3) -> List[Dict[str, Any]]:
    if not isinstance(travel_type_code, str):
        raise TypeError("travel_type_code는 문자열이어야 합니다.")
    if travel_type_code not in VALID_TRAVEL_TYPES:
        raise ValueError(f"지원하지 않는 여행 유형 코드입니다: {travel_type_code}")
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise TypeError("limit는 정수여야 합니다.")
    if limit < 1:
        raise ValueError("limit는 1 이상이어야 합니다.")

    travel_types = load_travel_types()
    travel_candidates = load_travel_candidates()
    places = load_place_dataset()

    keyword_order = travel_types[travel_type_code]["keywords"]
    ranked: List[Dict[str, Any]] = []

    for content_id, config in travel_candidates.items():
        if travel_type_code not in config.get("recommendedTypes", []):
            continue
        if config.get("reviewRequired", False):
            continue

        place = get_place_by_id(places, content_id)
        if place is None:
            raise ValueError(f"추천 후보 {content_id}에 해당하는 원본 Place 데이터가 없습니다.")

        tags = place.get("tags")
        if not isinstance(tags, list) or not tags:
            raise ValueError(f"추천 후보 {content_id}에 태그 정보가 없습니다.")

        matched_keywords = [keyword for keyword in keyword_order if keyword in tags]
        ranked.append({
            "contentId": str(content_id),
            "title": place.get("title", ""),
            "contentType": place.get("contentType", ""),
            "address": place.get("address", ""),
            "imageUrl": place.get("imageUrl", ""),
            "matchedKeywords": matched_keywords,
            "matchScore": len(matched_keywords),
        })

    ranked.sort(key=lambda item: (-item["matchScore"], item["contentId"]))
    result = []
    for item in ranked[:limit]:
        matched_keywords = item["matchedKeywords"]
        if matched_keywords:
            reason = f"선호 키워드인 {', '.join(matched_keywords)}와 잘 맞는 장소입니다."
        else:
            reason = "선택한 여행 유형에 맞는 추천 장소입니다."
        result.append({
            **item,
            "reason": reason,
        })

    return result
