from unittest import TestCase

from domain_layer.game_play.injects import Inject
from domain_layer.game_play.mock_interface import BranchingScenarioBuilder, MockScenarioBuilder
from domain_layer.common.injects import BaseChoiceInject
from domain_layer.scenario_design.scenarios import BaseStory, Story


class ScenarioTest(TestCase):
    def setUp(self) -> None:
        self.scenario = MockScenarioBuilder.build_scenario()

    def test_scenario_add_story(self):
        inject = BaseChoiceInject(label="test inject", text="text")
        story = BaseStory(title="introduction", entry_node=inject)

        scenario = BranchingScenarioBuilder.build_scenario()
        scenario.add_story(story)
        last_story = scenario.stories[len(scenario.stories) - 1]
        self.assertEqual(last_story, story)

    def test_scenario_vars(self):
        scenario = BranchingScenarioBuilder.build_scenario()
        scenario_vars = scenario.variables
        self.assertIsInstance(scenario_vars, dict)

    def test_set_description(self):
        description = "My description just changed"
        self.scenario.scenario_description = description
        self.assertEqual(self.scenario.scenario_description, description)

    def test_set_title(self):
        title = "A different title"
        self.scenario.title = title
        self.assertEqual(self.scenario.title, title)

    def test_set_target_group(self):
        target_group = "Engineers"
        self.scenario.target_group = target_group
        self.assertEqual(self.scenario.target_group, target_group)

    def test_set_story(self):
        stories = self.scenario.stories
        new_story = Story("A final chapter!", Inject(label="A final inject", text=""))
        stories.append(new_story)
        self.scenario.stories = stories
        self.assertEqual(self.scenario.stories[len(self.scenario.stories) - 1], new_story)
