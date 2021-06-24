from unittest import TestCase

from domain.scenario_design.scenario import Scenario
from domain.scenario_design.scenario_management import ScenarioFactory


class ScenarioFactoryTest(TestCase):

    def test_create_from_scratch(self):
        scenario = ScenarioFactory.create_scenario()
        self.assertIsInstance(scenario, Scenario)

    def test_create_scenario_from_dict(self):
        scenario_dict = {"title": "test scenario", "description": "some description", "scenario_id": "asd234sr32"}
        scenario = ScenarioFactory.build_scenario_from_dict(**scenario_dict)
        self.assertIsInstance(scenario, Scenario)
