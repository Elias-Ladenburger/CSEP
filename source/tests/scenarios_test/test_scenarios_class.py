from unittest import TestCase

from domain.game_play.mock_interface import BranchingScenarioBuilder
from domain.common.injects import BaseChoiceInject
from domain.scenario_design.scenario import Story


class ScenarioTest(TestCase):

    def test_scenario_add_story(self):
        inject = BaseChoiceInject(label="test inject", text="text")
        story = Story(title="introduction", entry_node=inject)

        scenario = BranchingScenarioBuilder.build_scenario()
        scenario.add_story(story)
        last_story = scenario.stories[len(scenario.stories)-1]
        self.assertEqual(last_story, story)

    def test_scenario_vars(self):
        scenario = BranchingScenarioBuilder.build_scenario()
        scenario_vars = scenario.variables
        self.assertIsInstance(scenario_vars, dict)

    def test_set_description(self):
        self.fail()

    def test_set_title(self):
        self.fail()

    def test_set_target_group(self):
        self.fail()

    def test_set_story(self):
        self.fail()



