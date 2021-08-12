import json
from unittest import TestCase

from application_layer.M2MTransformationService import InjectTransformer
from domain_layer.game_play.mock_interface import MockScenarioBuilder


class ScenarioPersistenceTest(TestCase):
    def setUp(self):
        pass

    def test_transform_inject_to_visjs(self):
        scenario = MockScenarioBuilder.build_scenario()
        injects = scenario.get_all_injects()
        transformed_injects = InjectTransformer.transform_injects_to_visjs(injects)
        print(transformed_injects)

