import unittest

from domain.scenario_design.game import Game
from domain.scenario_design.injects import PlainInject
from domain.scenario_design.scenario import Scenario, Story, StoryGraph
from domain.scenario_design.transitions import Transition


class InjectTest(unittest.TestCase):


    def test_create_game_with_only_informative_injects(self):
        second_last_inject = PlainInject(title="Almost Done", text="Welcome to the story!")
        last_inject = PlainInject(title="Finish", text="You have completed the scenario!")

        final_transition = Transition(from_inject=second_last_inject, to_inject=last_inject)

        final_graph = StoryGraph(injects=[second_last_inject, last_inject], transitions=[final_transition])
        final_chapter = Story(title="final chapter", entry_node=second_last_inject, story_graph=final_graph)

        intro_inject = PlainInject(title="Introduction", text="Welcome to the story!")
        second_inject = PlainInject(title="Second Inject", text="This is the second inject")
        first_to_second = Transition(from_inject=intro_inject, to_inject=second_inject)
        second_to_last = Transition(from_inject=second_inject, to_inject=second_last_inject)

        intro_graph = StoryGraph(injects=[intro_inject], transitions=[first_to_second, second_to_last])
        introduction = Story(title="introduction", entry_node=intro_inject, story_graph=intro_graph)

        scenario = Scenario(title="Going Phishing", description="A scenario where you capture credentials by phishing.")
        scenario.add_story(introduction)
        scenario.add_story(final_chapter)
        game = Game(scenario)
        print(game)
        self.assertTrue(game)

    def test_create_game_with_only_choice_injects(self):
        second_last_inject = PlainInject(title="Almost Done", text="Welcome to the story!")
        last_inject = PlainInject(title="Finish", text="You have completed the scenario!")

        final_transition = Transition(from_inject=second_last_inject, to_inject=last_inject, label="Walk straight ahead")
        other_final_transition = Transition(from_inject=second_last_inject, to_inject=last_inject, label="Turn left")

        final_graph = StoryGraph(injects=[second_last_inject, last_inject], transitions=[final_transition, other_final_transition])
        final_chapter = Story(title="final chapter", entry_node=second_last_inject, story_graph=final_graph)

        intro_inject = PlainInject(title="Introduction", text="Welcome to the story!")
        second_inject = PlainInject(title="Second Inject", text="This is the second inject")
        first_to_second = Transition(from_inject=intro_inject, to_inject=second_inject, label="Talk to the mayor")
        second_to_last = Transition(from_inject=second_inject, to_inject=second_last_inject, label="Do nothing")
        other_first_second = Transition(from_inject=intro_inject, to_inject=second_inject, label="Do nothing")
        other_second_third = Transition(from_inject=second_inject, to_inject=second_last_inject, label="Work stuff out")

        intro_graph = StoryGraph(injects=[intro_inject], transitions=[first_to_second, second_to_last, other_first_second, other_second_third])
        introduction = Story(title="introduction", entry_node=intro_inject, story_graph=intro_graph)

        scenario = Scenario(title="Going Phishing", description="A scenario where you capture credentials by phishing.")
        scenario.add_story(introduction)
        scenario.add_story(final_chapter)
        game = Game(scenario)
        print(game)
        self.assertTrue(game)
