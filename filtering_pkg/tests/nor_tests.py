import unittest
from unittest import skip

from filtering_pkg.collection import Collection


class NorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.collection = Collection()

    def test_1(self):
        self.assertEqual(
            "Papi",
            self.collection.find_one(
                {"$nor": [
                    {"$or": [
                        {"author": {"$eq": "Eliot"}},
                        {"author": {"$eq": "David"}}]},
                    {"author": "Papi2"}]}
                    ).get("author")
            )
