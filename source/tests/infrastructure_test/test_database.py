from unittest import TestCase

import bson

from infrastructure.database import CustomDB


class ScenarioPersistenceTest(TestCase):

    def setUp(self):
        self.db = CustomDB

    def tearDown(self):
        # self.db._purge_database(collection_name="scenarios")
        pass

    def test_database(self):
        scenarios_coll = self.db.get_collection_by_name("scenarios")
        self.assertIsNotNone(scenarios_coll)

    def test_insert(self):
        inserted_id = self.db.insert_one(collection_name="test", entity={"name": "test"})
        self.assertIsInstance(inserted_id.inserted_id, bson.ObjectId)
