import json
import unittest
from pathlib import Path
from unittest.mock import patch

from data.travel_recommender import (
    load_travel_candidates,
    load_travel_types,
    recommend_places,
)


class TravelRecommenderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = Path(__file__).resolve().parents[1]
        cls.travel_types = load_travel_types()
        cls.travel_candidates = load_travel_candidates()
        cls.place_tags = json.loads((cls.base_dir / "data/derived/place_tags.json").read_text(encoding="utf-8"))

    def test_recommendations_exist_for_all_travel_types(self):
        for travel_type in ["HEALING", "EXPLORER", "CULTURE", "FOODIE"]:
            recommendations = recommend_places(travel_type, limit=3)
            self.assertTrue(recommendations, msg=f"{travel_type} 추천 결과가 없습니다")

    def test_limit_controls_result_count(self):
        recommendations = recommend_places("HEALING", limit=5)
        self.assertLessEqual(len(recommendations), 5)

        smaller = recommend_places("HEALING", limit=1)
        self.assertLessEqual(len(smaller), 1)

    def test_review_required_and_type_filtering(self):
        recommendations = recommend_places("HEALING", limit=10)
        self.assertTrue(recommendations)
        self.assertTrue(all(item["contentId"] != "2736676" for item in recommendations))
        self.assertTrue(all(item["contentId"] != "2782877" for item in recommendations))

        explorer_recommendations = recommend_places("EXPLORER", limit=10)
        self.assertTrue(all(item["contentId"] != "3302702" for item in explorer_recommendations))

    def test_results_are_sorted_by_score_then_content_id(self):
        recommendations = recommend_places("HEALING", limit=10)
        scores = [item["matchScore"] for item in recommendations]
        self.assertEqual(scores, sorted(scores, reverse=True))

        for index in range(len(recommendations) - 1):
            if recommendations[index]["matchScore"] == recommendations[index + 1]["matchScore"]:
                self.assertLess(recommendations[index]["contentId"], recommendations[index + 1]["contentId"])

    def test_matched_keywords_and_reason_are_deterministic(self):
        recommendations = recommend_places("HEALING", limit=5)
        self.assertTrue(recommendations)

        for item in recommendations:
            keywords = self.travel_types["HEALING"]["keywords"]
            expected_keywords = [keyword for keyword in keywords if keyword in self.place_tags[item["contentId"]]]
            self.assertEqual(item["matchedKeywords"], expected_keywords)
            self.assertEqual(item["matchScore"], len(expected_keywords))

            if expected_keywords:
                self.assertEqual(
                    item["reason"],
                    f"선호 키워드인 {', '.join(expected_keywords)}와 잘 맞는 장소입니다.",
                )
            else:
                self.assertEqual(item["reason"], "선택한 여행 유형에 맞는 추천 장소입니다.")

    def test_result_fields_match_api_spec_shape(self):
        recommendation = recommend_places("FOODIE", limit=1)[0]
        self.assertEqual(
            set(recommendation.keys()),
            {"contentId", "title", "contentType", "address", "imageUrl", "matchedKeywords", "matchScore", "reason"},
        )
        self.assertIsInstance(recommendation["matchedKeywords"], list)
        self.assertIsInstance(recommendation["matchScore"], int)
        self.assertIsInstance(recommendation["reason"], str)

    def test_invalid_travel_type_and_limit_raise_errors(self):
        with self.assertRaises(ValueError):
            recommend_places("UNKNOWN")

        with self.assertRaises(ValueError):
            recommend_places("HEALING", limit=0)

        with self.assertRaises(ValueError):
            recommend_places("HEALING", limit=-1)

        with self.assertRaises(TypeError):
            recommend_places("HEALING", limit="3")

    def test_same_input_returns_same_result(self):
        first = recommend_places("EXPLORER", limit=3)
        second = recommend_places("EXPLORER", limit=3)
        self.assertEqual(first, second)

    def test_empty_tags_raise_value_error(self):
        with patch("data.travel_recommender.get_place_by_id") as mock_get_place_by_id:
            from data.place_loader import load_place_dataset

            places = load_place_dataset()
            original_place = next(place for place in places if place["contentId"] == "3032819")
            empty_tag_place = {**original_place, "tags": []}

            def get_place_by_id_override(places_arg, content_id):
                if str(content_id) == "3032819":
                    return empty_tag_place
                return next((place for place in places_arg if place["contentId"] == str(content_id)), None)

            mock_get_place_by_id.side_effect = get_place_by_id_override

            with self.assertRaises(ValueError):
                recommend_places("HEALING", limit=1)


if __name__ == "__main__":
    unittest.main()
