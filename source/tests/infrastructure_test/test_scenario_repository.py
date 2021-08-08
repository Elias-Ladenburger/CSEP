from unittest import TestCase

from domain_layer.common.scenarios import BaseScenario
from domain_layer.game_play.mock_interface import MockScenarioBuilder
from domain_layer.common.injects import BaseChoiceInject
from domain_layer.scenario_design.injects import EditableInject
from domain_layer.scenario_design.scenario_management import EditableScenarioRepository
from domain_layer.scenario_design.scenarios import EditableScenario, BaseStory, Story
from domain_layer.common.scenario_management import ScenarioRepository, ScenarioFactory
from infrastructure_layer.database import CustomDB


class ScenarioPersistenceTest(TestCase):

    def setUp(self):
        test_env = "DEV"
        from globalconfig import config
        config.set_env(test_env)
        self.repo = ScenarioRepository
        test_scenario = MockScenarioBuilder.build_scenario()
        self.test_scenario = self.repo.save_scenario(test_scenario)
        self.db = CustomDB
        print("Test Config: {}".format(test_env))

    def tearDown(self):
        #
        # self.db._purge_database(collection_name="scenarios")
        pass

    def test_insert_scenario_title_description(self):
        scenario = ScenarioFactory.create_scenario(title="yay!", description="This is a new scenario")
        self.assertIsNotNone(scenario.scenario_id)

    def test_delete_scenario(self):
        ScenarioRepository.delete_by_id(self.test_scenario.scenario_id)

    def test_get_scenario(self):
        scenario = ScenarioFactory.create_scenario(title="test", description="test")
        scenario_id = self.repo.save_scenario(scenario).scenario_id
        scenario = self.repo.get_scenario_by_id(scenario_id=scenario_id)
        if scenario:
            print(scenario.dict())
        self.assertIsInstance(scenario, BaseScenario)

    def test_get_all_scenarios(self):
        all_scenarios = self.repo.get_all_scenarios()
        if all_scenarios:
            print(next(all_scenarios))
        self.assertIsNotNone(all_scenarios)

    def test_update_scenario_change_title(self):
        self.test_scenario.title = "Changed title!"
        inserted_id = self.repo.save_scenario(self.test_scenario).scenario_id
        new_scenario = self.repo.get_scenario_by_id(inserted_id)
        self.assertEqual(new_scenario.title, "Changed title!")

    def test_multiple_collections(self):
        pass

    def test_insert_scenario_with_stories(self):
        inserted_id = self.insert_scenario_with_stories()
        self.assertIsInstance(inserted_id, str)

    def test_load_scenario(self):
        inserted_id = self.insert_scenario_with_stories()
        scenario = self.repo.get_scenario_by_id(inserted_id)
        self.assertIsInstance(scenario, BaseScenario)

    def test_load_story(self):
        inserted_id = self.insert_scenario_with_stories()
        scenario = self.repo.get_scenario_by_id(inserted_id)
        story = scenario.stories[0]
        self.assertIsInstance(story, BaseStory)

    def test_load_inject(self):
        inserted_id = self.insert_scenario_with_stories()
        scenario = self.repo.get_scenario_by_id(inserted_id)
        inject = scenario.get_inject_by_slug("introduction")
        self.assertIsInstance(inject, BaseChoiceInject)

    def insert_scenario_with_stories(self):
        scenario = MockScenarioBuilder.build_scenario()
        inserted_id = self.repo.save_scenario(scenario).scenario_id
        return inserted_id

    def test_modify_scenario(self):
        original_scenario = EditableScenarioRepository.get_scenario_by_id(scenario_id=self.test_scenario.scenario_id)

        scenario = EditableScenario(**original_scenario.dict())
        inject = EditableInject(label="First inject", text="Inject Text")
        story = Story("Test Story", entry_node=inject)
        scenario.add_story(story)
        ScenarioRepository.save_scenario(scenario)
        changed_scenario = EditableScenarioRepository.get_scenario_by_id(scenario_id=self.test_scenario.scenario_id)
        print(changed_scenario.target_group)
        self.assertTrue(changed_scenario.target_group == original_scenario.target_group)
