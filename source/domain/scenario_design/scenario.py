from enum import Enum
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
        self._entry_node = entry_node
        self.story_graph = story_graph

    def add_inject(self, inject: Inject):
        self.story_graph.injects.append(inject)

    def remove_inject(self, inject: Inject):
        self.story_graph.injects.remove(inject)

    def add_transition(self, transition: Transition):
        self.story_graph.transitions.append(transition)

    def remove_transition(self, transition: Transition):
        self.story_graph.transitions.remove(transition)

    def set_entry_node(self, new_entry: Inject):
        self._entry_node = new_entry

    def get_entry(self):
        return self._entry_node

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if isinstance(title, str):
            self._title = title
        else:
            raise TypeError

    def __str__(self):
        return_str = "Story: " + self.title
        for transition in self.story_graph.transitions:
            return_str += "\n" + str(transition)
        return return_str


class DataType(Enum):
    TEXT = 1
    NUMBER = 2
    BOOL = 3


class ScenarioVariable:
    """A variable that simulates the environment of a scenario."""
    def __init__(self, name: str, datatype: DataType, hidden: bool = False):
        self.name = name
        self.datatype = datatype
        self.hidden = hidden

    def is_value_legal(self, value):
        if self.datatype == DataType.TEXT:
            if isinstance(value, str):
                return True
        elif self.datatype == DataType.NUMBER:
            if isinstance(value, float) or isinstance(value, int):
                return True
        elif self.datatype == DataType.BOOL:
            if isinstance(value, bool):
                return True
        return False

class Scenario:
    """A container for multiple stories"""
    def __init__(self, title: str, description: str):
        """

        :param title: How this scenario_design is called
        :param description: A brief human-understandable description of the scenario_design
        :param stories: An unordered list of the the stories that make up this scenario_design
        """
        self.title = title
        self.description = description
        self.stories = list()
        self.variables = dict()

    def add_story(self, story: Story):
        self.stories.append(story)

    def remove_story(self, story: Story):
        self.stories.remove(story)
    
    def add_variable(self, var: ScenarioVariable, starting_value = None):
        self.variables[var] = starting_value
    
    def remove_variable(self, var: ScenarioVariable):
        self.variables.pop(var)
