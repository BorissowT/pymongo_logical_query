import unittest
from unittest import skip

from filtering_pkg.collection import Collection


class OrTest(unittest.TestCase):
    def setUp(self) -> None:
        self.collection = Collection()

    def test_eq_1(self):
        self.assertEqual(
            "Papi",
            self.collection.find_one(
            {"$or": [{"author": {"$eq": "Papi"}}, {"id": {"$eq": 15}}]}
                ).get("author")
            )

    def test_eq_2(self):
        self.assertGreater(
            12,
            self.collection.find_one(
                {"$or": [{"rating": {"$lt": 12}}, {"rating": 10}]}
            ).get("rating")
        )

    def test_gt_1(self):
        self.assertEqual(
            {"author": "David", "title": "some4", "rating": 11, "id": 9},
            self.collection.find_one(
                {"$or": [{"rating": {"$gt": 110}}, {"id": {"$eq": 9}}]})
        )

    def test_gt_2(self):
        self.assertLess(75,
                        self.collection.find_one(
                        {"$or": [{"rating": {"$gt": 75}}, {"id": {"$eq": 92}}]}
                                                ).get("rating")
        )

    def test_gte(self):
        self.assertLessEqual(76,
                             self.collection.find_one(
            {"$or": [{"rating": {"$gte": 76}}, {"id": {"$eq": 92}}]}
                             ).get("rating"),
        )

    def test_lt(self):
        self.assertEqual(self.collection.find_one(
            {"$or": [{"rating": {"$lt": 11}}, {"title": {"$eq": "crazy"}}]}),
        {"author": "Papi", "title": "some4", "rating": 10, "id": 15},
        )

    def test_lte(self):
        self.assertEqual(self.collection.find_one(
            {"$or": [{"rating": {"$lte": 10}}, {"title": {"$eq": "crazy"}}]}),
        {"author": "Papi", "title": "some4", "rating": 10, "id": 15},
        )

    def test_ne_and_nested(self):
        # not david and not eliot and not papi2-> Papi!
        self.assertEqual(self.collection.find_one(
            {"$or": [
                {"$and": [{"author": {"$ne": "David"}},
                         {"author": {"$ne": "Eliot"}},
                          {"author": {"$ne": "Papi2"}}]},
                {"id": 100}
                ]
            }
        ),
            {"author": "Papi", "title": "some4", "rating": 10, "id": 15},
        )

    @skip("s")
    def test_example(self):
        self.assertEqual()
