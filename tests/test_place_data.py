import unittest

from data.place_loader import filter_places, get_place_by_id, load_place_dataset


class PlaceDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.places = load_place_dataset()

    def test_loads_all_raw_files_and_counts(self):
        self.assertEqual(len(self.places), 1667)
        self.assertEqual(len({place['contentId'] for place in self.places}), len(self.places))

    def test_normalizes_place_shape_and_safely_handles_missing_data(self):
        place = get_place_by_id(self.places, '3032819')
        self.assertIsNotNone(place)
        self.assertEqual(place['contentId'], '3032819')
        self.assertEqual(place['contentType'], '관광지')
        self.assertEqual(place['region'], '구미')
        self.assertEqual(place['address'], '경상북도 구미시 황상동')
        self.assertEqual(place['detailAddress'], '')
        self.assertEqual(place['telephone'], '')
        self.assertIsInstance(place['longitude'], float)
        self.assertIsInstance(place['latitude'], float)
        self.assertIsInstance(place['tags'], list)

    def test_filters_and_keyword_search(self):
        filtered_type = filter_places(self.places, content_type='관광지')
        self.assertTrue(filtered_type)
        self.assertTrue(all(place['contentType'] == '관광지' for place in filtered_type))

        filtered_region = filter_places(self.places, region='구미')
        self.assertTrue(filtered_region)
        self.assertTrue(all(place['region'] == '구미' for place in filtered_region))

        filtered_keyword = filter_places(self.places, keyword='생태')
        self.assertTrue(filtered_keyword)
        self.assertTrue(any('생태' in place['title'] for place in filtered_keyword))


if __name__ == '__main__':
    unittest.main()
