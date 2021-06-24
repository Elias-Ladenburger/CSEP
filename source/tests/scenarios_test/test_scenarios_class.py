import json
from unittest import TestCase

from domain.game_play.mock_interface import BranchingScenarioBuilder
from domain.scenario_design.injects import Inject
from domain.scenario_design.scenario import Story


class ScenarioTest(TestCase):

    def test_scenario_add_story(self):
        inject = Inject(title="test inject", text="text")
        story = Story(title="introduction", entry_node=inject, injects=[inject], transitions=[])

        scenario = BranchingScenarioBuilder.build_scenario()
        scenario.add_story(story)
        last_story = scenario.stories[len(scenario.stories)-1]
        self.assertEqual(last_story, story)

    def test_scenario_vars(self):
        scenario = BranchingScenarioBuilder.build_scenario()
        print(vars(scenario))

    def test_examine_scenario_properties(self):
        scenario = BranchingScenarioBuilder.build_scenario()
        print(scenario.__dict__)
        print(scenario.stories[0].__dict__)
        print(scenario.stories[0].entry_node.__dict__)
        print(scenario.stories[0].entry_node.transitions[0].__dict__)

