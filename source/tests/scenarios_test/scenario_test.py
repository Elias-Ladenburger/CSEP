import unittest

from domain.scenario_design.scenario import Story, Inject, StoryGraph, Transition


class StoryTest(unittest.TestCase):

    def test_create_scenario_valid_plain(self):
        story = Story(title="newStory", entry_node=Inject("new Inject"), story_graph=None)
        self.assertTrue(isinstance(story, Story))

    def test_create_scenario_valid_plain_no_graph(self):
        story = Story(title="newStory", entry_node=Inject("new Inject"))
        self.assertTrue(isinstance(story, Story))

    def test_create_scenario_exit_missing(self):
        try:
            story = Story(title="newStory", entry_node=Inject("new Inject"))
        except(TypeError):
            self.assertTrue(True)
        self.assertTrue(False)

    def test_delete_inject(self):
        self.assertTrue(False)

    def test_change_inject(self):
        self.assertTrue(False)

    def test_create_complete_scenario(self):
        inject_intro = Inject(title="intro inject", description="Welcome to this scenario_design!")
        inject_last = Inject(title="last inject", description="Thank you for playing the scenario_design!")
        intro_graph = StoryGraph(injects=[inject_intro], transitions=[Transition(from_inject=inject_intro, to_inject=inject_last)])
        story_introduction = Story(title="introduction", entry_node=inject_intro, story_graph=intro_graph)
