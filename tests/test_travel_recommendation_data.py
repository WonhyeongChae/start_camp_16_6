import json
import unittest
from pathlib import Path

from data.place_loader import load_place_dataset


class TravelRecommendationDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = Path(__file__).resolve().parents[1]
        cls.places = load_place_dataset()
        cls.place_tags = json.loads((cls.base_dir / "data/derived/place_tags.json").read_text(encoding="utf-8"))
        cls.travel_types = json.loads((cls.base_dir / "data/derived/travel_types.json").read_text(encoding="utf-8"))
        cls.travel_candidates = json.loads((cls.base_dir / "data/derived/travel_candidates.json").read_text(encoding="utf-8"))
        cls.allowed_tags = {tag for config in cls.travel_types.values() for tag in config["keywords"]}

    def test_tags_are_within_allowed_tag_set(self):
        for content_id, tags in self.place_tags.items():
            for tag in tags:
                self.assertIn(tag, self.allowed_tags)

    def test_candidate_content_ids_exist_in_source_and_tags(self):
        content_ids = {place["contentId"] for place in self.places}
        for content_id in self.travel_candidates:
            self.assertIn(content_id, content_ids)
            self.assertIn(content_id, self.place_tags)

    def test_each_travel_type_has_at_least_three_candidates(self):
        counts = {travel_type: 0 for travel_type in self.travel_types}
        for content_id, config in self.travel_candidates.items():
            for travel_type in config["recommendedTypes"]:
                counts[travel_type] += 1

        for travel_type, count in counts.items():
            self.assertGreaterEqual(count, 3, msg=f"{travel_type} 후보 수가 부족합니다")

    def test_candidate_structure_and_tag_rules(self):
        self.assertLessEqual(len(self.travel_candidates), 30)

        valid_types = set(self.travel_types)
        for content_id, config in self.travel_candidates.items():
            self.assertTrue(isinstance(config["reviewRequired"], bool))
            self.assertLessEqual(len(config["recommendedTypes"]), 2)
            for travel_type in config["recommendedTypes"]:
                self.assertIn(travel_type, valid_types)

            tags = self.place_tags[content_id]
            self.assertGreaterEqual(len(tags), 1)
            self.assertEqual(len(tags), len(set(tags)))

        foodies = [content_id for content_id, config in self.travel_candidates.items() if "FOODIE" in config["recommendedTypes"]]
        self.assertTrue(foodies)
        for content_id in foodies:
            tags = self.place_tags[content_id]
            self.assertTrue(any(tag in {"음식점", "시장", "특산물"} for tag in tags))

        cultures = [content_id for content_id, config in self.travel_candidates.items() if "CULTURE" in config["recommendedTypes"]]
        self.assertTrue(cultures)
        for content_id in cultures:
            tags = self.place_tags[content_id]
            self.assertTrue(any(tag in {"문화", "역사", "전시"} for tag in tags))

        self.assertTrue(all(keyword in self.allowed_tags for keyword in {tag for config in self.travel_types.values() for tag in config["keywords"]}))


if __name__ == "__main__":
    unittest.main()
