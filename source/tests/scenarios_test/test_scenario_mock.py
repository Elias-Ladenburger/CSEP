from unittest import TestCase

from domain.game_play.mock_interface import MockScenarioBuilder
from domain.scenario_design.scenarios import EditableScenario
from domain.common.scenario_management import ScenarioFactory
from infrastructure.database import CustomDB


class ScenarioMock(TestCase):
    def setUp(self) -> None:
        from globalconfig import config
        config.set_env("TEST")

    def tearDown(self) -> None:
        CustomDB._purge_database("scenarios")
        pass

    def test_create_single_scenario(self):
        test_scenario = MockScenarioBuilder.build_scenario()
        self.assertIsInstance(test_scenario, EditableScenario)

    def test_create_two_scenarios_with_id(self):
        scenario1 = ScenarioFactory.create_scenario(title="test", description="a description", scenario_id="31231asa")
        scenario2 = ScenarioFactory.create_scenario(title="test", description="a description", scenario_id="anotherid")
        self.assertNotEqual(scenario1, scenario2)

    def test_create_two_mock_scenarios_without_id(self):
        scenario1 = MockScenarioBuilder.build_scenario()
        scenario2 = MockScenarioBuilder.build_scenario()
        print(scenario1)
        print(scenario2)
        self.assertEqual(scenario1, scenario2)

