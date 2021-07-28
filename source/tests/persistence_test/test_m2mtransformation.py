from unittest import TestCase

from domain.game_play.mock_interface import MockScenarioBuilder
from domain.scenario_design.injects import Inject
from infrastructure.database import CustomDB


class DictConversionTest(TestCase):
    def setUp(self) -> None:
        from globalconfig import config
        config.set_env("TEST")
        self.test_scenario = MockScenarioBuilder.build_scenario()

    def tearDown(self) -> None:
        CustomDB._purge_database("scenarios")

    def test_inject_as_dict(self):
        test_entity = self.test_scenario.stories[0].entry_node
        self.assert_entity_converts_to_dict(test_entity)

    def test_story_as_dict(self):
        test_entity = self.test_scenario.stories[0]
        self.assert_entity_converts_to_dict(test_entity)

    def test_scenario_as_dict(self):
        test_entity = self.test_scenario
        self.assert_entity_converts_to_json(test_entity)

    def assert_entity_converts_to_dict(self, test_entity):
        my_dict = test_entity.dict()
        print(my_dict)
        self.assertIsInstance(my_dict, dict)

    def assert_entity_converts_to_json(self, test_entity):
        print(test_entity)
        my_json = test_entity.json(indent=2)
        print(my_json)
        self.assertIsInstance(my_json, str)
