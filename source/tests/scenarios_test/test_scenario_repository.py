from unittest import TestCase

from domain.game_play.mock_interface import MockScenarioBuilder
from domain.scenario_design.scenario import Scenario
from domain.scenario_design.scenario_management import ScenarioRepository, ScenarioFactory
from globalconfig import config
from infrastructure.database import CustomDB


class ScenarioPersistenceTest(TestCase):

    def setUp(self):
        config.set_env("TEST")
        self.repo = ScenarioRepository
        self.test_scenario = MockScenarioBuilder.build_scenario()
        self.db = CustomDB

    def tearDown(self):
        # self.db._purge_database(collection_name="scenarios")
        pass

    def test_insert_scenario_title_description(self):
        scenario = ScenarioFactory.create_scenario(title="yay!", description="This is a new scenario")
        self.assertIsNotNone(scenario.scenario_id)

    def test_delete_scenario(self):
        pass

    def test_get_scenario(self):
        scenario = ScenarioFactory.create_scenario(title="test", description="test")
        scenario_id = scenario.scenario_id
        scenario = self.repo.get_scenario_by_id(scenario_id=scenario_id)
        if scenario:
            print(scenario.dict())
        self.assertIsInstance(scenario, Scenario)

    def test_get_all_scenarios(self):
        all_scenarios = self.repo.get_all_scenarios()
        if all_scenarios:
            print(all_scenarios[0])
        self.assertIsNotNone(all_scenarios)

    def test_update_scenario_add_story(self):
        inserted_id = self.test_scenario.scenario_id
        self.test_scenario.title = "Changed title!"
        self.repo.save_scenario(self.test_scenario)
        new_scenario = self.repo.get_scenario_by_id(inserted_id)
        self.assertEqual(new_scenario.title, "Changed title!")
