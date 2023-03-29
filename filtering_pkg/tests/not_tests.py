import unittest
from unittest import skip

from filtering_pkg.collection import ICollection


class NotTest(unittest.TestCase):
    def setUp(self) -> None:
        self.collection = ICollection()

    def test_1(self):
        self.assertNotEqual(
            "Eliot",
            self.collection.find_one(
                {"$not": [{"author": {"$eq": "Eliot"}}]}
                    ).get("author")
            )
