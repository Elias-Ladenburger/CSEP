from unittest import TestCase

import bson

from domain.scenario_design.scenario import Scenario, ScenarioRepository
from globalconfig import config


class ScenarioPersistenceTest(TestCase):

    def setUp(self):
        config.set_env("TEST")
        self.repo = ScenarioRepository

    def tearDown(self):
        # self.db._purge_database(collection_name="scenarios")
        pass

    def test_insert_scenario(self):
        scenario = Scenario(title="new scenario", description="yay!")
        insertion_result = self.repo.save_scenario(scenario)
        self.assertIsInstance(insertion_result.inserted_id, bson.ObjectId)

    def test_delete_scenario(self):
        pass

    def test_get_scenario(self):
        pass

    def test_get_all_scenarios(self):
        all_scenarios = self.repo.get_all_scenarios()
        self.assertIsNotNone(all_scenarios)

    def test_returns_scenarios(self):
        all_scenarios = self.repo.get_all_scenarios()
