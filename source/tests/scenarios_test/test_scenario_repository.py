import json
from unittest import TestCase

from domain.game_play.mock_interface import MockScenarioBuilder
from domain.scenario_design.scenario import Scenario
from domain.scenario_design.scenario_management import ScenarioRepository, ScenarioFactory
from infrastructure.database import CustomDB


class ScenarioPersistenceTest(TestCase):

    def setUp(self):
        from globalconfig import config
        config.set_env("DEV")
        self.repo = ScenarioRepository
        self.test_scenario = MockScenarioBuilder.build_scenario()
        self.repo.save_scenario(self.test_scenario)
        self.db = CustomDB

    def tearDown(self):
        self.db._purge_database(collection_name="scenarios")
        pass

    def test_insert_scenario_title_description(self):
        scenario = ScenarioFactory.create_scenario(title="yay!", description="This is a new scenario")
        self.assertIsNotNone(scenario.scenario_id)

    def test_delete_scenario(self):
        pass

    def test_get_scenario(self):
        scenario = ScenarioFactory.create_scenario(title="test", description="test")
        scenario_id = self.repo.save_scenario(scenario)
        scenario = self.repo.get_scenario_by_id(scenario_id=scenario_id)
        if scenario:
            print(scenario.dict())
        self.assertIsInstance(scenario, Scenario)

    def test_get_all_scenarios(self):
        all_scenarios = self.repo.get_all_scenarios()
        if all_scenarios:
            print(all_scenarios[0])
        self.assertIsNotNone(all_scenarios)

    def test_update_scenario_change_title(self):
        inserted_id = self.test_scenario.scenario_id
        self.test_scenario.title = "Changed title!"
        inserted_id = self.repo.save_scenario(self.test_scenario)
        new_scenario = self.repo.get_scenario_by_id(inserted_id)
        self.assertEqual(new_scenario.title, "Changed title!")

    def test_insert_scenario_with_stories(self):
        inserted_id = self.insert_scenario_with_stories()
        self.assertIsInstance(inserted_id, str)

    def test_load_scenario(self):
        inserted_id = self.insert_scenario_with_stories()
        scenario = self.repo.get_scenario_by_id(inserted_id)
        print(scenario.dict())
        self.assertIsInstance(scenario, Scenario)

    def insert_scenario_with_stories(self):
        scenario = MockScenarioBuilder.build_scenario()
        print(json.dumps(scenario.dict(), indent=2))
        inserted_id = self.repo.save_scenario(scenario)
        return inserted_id
