import unittest
from unittest import skip

from filtering_pkg.collection import ICollection


class AndTest(unittest.TestCase):
    def setUp(self) -> None:
        self.collection = ICollection()

    def test1(self):
        self.assertEqual(self.collection.find_one({"author": "Eliot"}),
            {"author": "Eliot", "title": "some", "rating": 54, "id": 1})

    def test2(self):
        self.assertEqual(
            "Eliot",
            self.collection.find_one(
                {"$and": [{
                    "author": "Eliot"},
                    {
                        "title": {"$eq": "some"}
                    }]
                }).get("author")
        )

    def test_3(self):
        self.assertEqual(self.collection.find_one(
            {"author": "Eliot", "title": "some2"}),
            {"author": "Eliot", "title": "some2", "rating": 30, "id": 2})

    def test_4(self):
        self.assertEqual(self.collection.find_one(
            {"$and": [{"rating": {"$gt": 65}}, {"id": {"$eq": 10}}]}),
            {"author": "David", "title": "some", "rating": 66, "id": 10},
            f"""result: {
            self.collection.find_one({"$and": [{"rating": {"$gt": 65}},
                                                       {"id": {"$eq": 10}}]})}
                                                       """
        )

    def test_5(self):
        self.assertEqual(self.collection.find_one(
            {"$and": [{"author": "David"}, {"rating": 66}]}),
            {"author": "David", "title": "some", "rating": 66, "id": 10}
        )

    def test_6(self):
        self.assertEqual(self.collection.find_one(
            {"$and": [{"rating": {"$eq": 11}}, {"id": {"$ne": 4}}]}),
            {"author": "David", "title": "some4", "rating": 11, "id": 9}
        )

    def test_7(self):
        self.assertEqual(
            {"author": "Eliot", "title": "some", "rating": 54, "id": 1},
            self.collection.find_one({
            "$and": [
                {"$and": [{"rating": {"$eq": 54}}, {"id": {"$ne": 6}}]},
                {"$and": [{"author": "Eliot"}, {"title": {"$eq": "some"}}]}
            ]
        }))

    def test_8(self):
        self.assertEqual(self.collection.find_one({"rating": {"$gte": 76}}),
            {"author": "David", "title": "some", "rating": 76, "id": 13},
            f"""result: {self.collection.find_one({"rating": {"$gte": 76}})}"""
                         )

    def test_9(self):
        self.assertGreater(
            12,
            self.collection.find_one(
            {
                "$and": [
                    {"rating": {"$lt": 12}},
                    {"id": {"$ne": 9}}
                ]
            }).get("rating"),
            f"""result: {self.collection.find_one(
                {"$and": [{"rating": {"$lt": 12}},{"id": {"$ne": 9}}]})}"""
        )

    def test_10(self):
        self.assertGreaterEqual(11, self.collection.find_one(
            {"$and": [{"rating": {"$lte": 11}}, {"id": {"$ne": 4}}]}
        ).get("rating"))

    @skip("s")
    def test_example(self):
        self.assertEqual()
