from unittest import TestCase

import bson

from domain.game_play.mock_interface import MockGameProvider
from domain.scenario_design.scenario import Scenario, ScenarioRepository
from globalconfig import config


class ScenarioPersistenceTest(TestCase):

    def setUp(self):
        config.set_env("TEST")
        self.repo = ScenarioRepository
        self.test_scenario = MockGameProvider.get_branching_game()

    def tearDown(self):
        # self.db._purge_database(collection_name="scenarios")
        pass

    def test_insert_scenario_title_description(self):
        scenario = Scenario(title="new scenario", description="yay!")
        insertion_result = self.repo.save_scenario(scenario)
        self.assertIsInstance(insertion_result, bson.ObjectId)

    def test_delete_scenario(self):
        pass

    def test_get_scenario(self):
        scenario = self.repo.get_scenario_by_id(scenario_id="60d1c25ad69078407bfcafaf")
        print(vars(scenario))
        self.assertIsInstance(scenario, Scenario)

    def test_get_all_scenarios(self):
        all_scenarios = self.repo.get_all_scenarios()
        print(all_scenarios[0])
        self.assertIsNotNone(all_scenarios)

    def test_update_scenario_add_story(self):
        inserted_id = self.repo.save_scenario(self.test_scenario)
        self.test_scenario.title = "Changed title!"
        self.repo.save_scenario(self.test_scenario)
