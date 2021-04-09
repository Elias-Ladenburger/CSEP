from typing import List

from domain.scenario_design.graphs import Graph
from domain.scenario_design.injects import Inject
from domain.scenario_design.transitions import Transition


class StoryGraph(Graph):
    """A collection of injects and transitions within a story"""
    def __init__(self, injects=List[Inject], transitions=List[Transition]):
        super().__init__()
        self.injects = injects
        self.transitions = transitions


class Story:
    """A _Story_ is a collection of injects within a scenario_design"""

    def __init__(self, title: str, entry_node: Inject, story_graph: StoryGraph):
        """
        :param title: A short descriptive title of the story to be able to gauge what it is about
        :param entry_node: the first inject that is shown when this story is started
        :param story_graph: the graph of all injects that are part of this story
        """
        self._title = title
        self.entry_node = entry_node
        self.story_graph = story_graph

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if isinstance(title, str):
            self._title = title
        else:
            raise TypeError

class Scenario:
    """A container for multiple stories"""
    def __init__(self, title: str, description: str, stories: List[Story]):
        """

        :param title: How this scenario_design is called
        :param description: A brief human-understandable description of the scenario_design
        :param stories: An ordered list of the the stories that make up this scenario_design
        """
        self.title = title
        self.description = description
        self.stories = stories

class ScenarioPlayer:
    """This class will handle how a scenario_design is played"""

    def __init__(self, scenario: Scenario):
        self.scenario = scenario

    def play(self):
        for story in self.scenario.stories:
            story.show_next()