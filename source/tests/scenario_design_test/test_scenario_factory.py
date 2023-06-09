from unittest import TestCase

from domain_layer.common.scenarios import BaseScenario
from domain_layer.scenariodesign.scenario_management import EditableScenarioFactory
from domain_layer.scenariodesign.scenarios import EditableScenario
from domain_layer.common.scenario_management import ScenarioFactory


class ScenarioFactoryTest(TestCase):

    def test_create_from_scratch(self):
        scenario = ScenarioFactory.create_scenario()
        self.assertIsInstance(scenario, BaseScenario)

    def test_create_scenario_from_dict(self):
        scenario_dict = {"title": "test scenario_design", "description": "some description", "scenario_id": "asd234sr32"}
        scenario = EditableScenarioFactory.build_from_dict(**scenario_dict)
        self.assertIsInstance(scenario, EditableScenario)
