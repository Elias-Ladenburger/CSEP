from enum import Enum
from typing import List

from domain.scenario_design.auxiliary import ScenarioVariable
from domain.scenario_design.graphs import GraphNode
from domain.scenario_design.injects import PlainInject, Transition


class Story(GraphNode):
    """A _Story_ is a collection of injects within a scenario_design"""

    def __init__(self, title: str, entry_node: PlainInject,
                 injects: List[PlainInject] = [], transitions: List[Transition] = []):
        """
        :param title: A short descriptive title of the story to be able to gauge what it is about
        :param entry_node: the first inject that is shown when this story is started
        :param injects: an unordered list of injects that are part of the story
        """
        super().__init__(label=title)
        self.entry_node = entry_node
        self._injects = {}
        self._transitions = {}
        self._initialize_injects(injects)
        self._initialize_transitions(transitions)

    def add_inject(self, inject: PlainInject):
        self._injects[inject.inject_id] = inject
        self._transitions[inject.inject_id] = []

    def remove_inject(self, inject: PlainInject):
        self._injects.pop(inject.inject_id)
        self._transitions.pop(inject.inject_id)
        for other_injects in self._transitions:
            for dangling_transition in self._transitions[other_injects]:
                if dangling_transition.to_inject == inject:
                    self._transitions[other_injects].remove(dangling_transition)

    def remove_inject_by_id(self, inject_id):
        self._injects.pop(inject_id)

    def get_inject_by_id(self, inject_id):
        if inject_id in self._injects:
            inject = self._injects[inject_id]
            transitions = self._transitions.get(inject_id, None)
            return inject, transitions
        return None

    def add_transition(self, transition: Transition):
        inject_transitions = self._transitions.get(transition.from_inject.inject_id, None)
        if inject_transitions:
            self._transitions[transition.from_inject.inject_id].append(transition)
        else:
            self._transitions[transition.from_inject.inject_id] = [transition]

    def add_transitions(self, transitions: List[Transition]):
        for transition in transitions:
            self.add_transition(transition)

    def remove_transition(self, transition):
        viable_transitions = self._transitions.get(transition.from_inject.inject_id, [])
        viable_transitions.remove(transition)

    def _initialize_injects(self, injects: List[PlainInject]):
        self.add_inject(self.entry_node)
        for inject in injects:
            self.add_inject(inject)

    def _initialize_transitions(self, transitions: List[Transition]):
        for transition in transitions:
            self.add_transition(transition)


class Scenario:
    """A container for multiple stories"""
    def __init__(self, title: str, description: str):
        """
        :param title: How this scenario_design is called
        :param description: A brief human-understandable description of the scenario_design
        """
        self.title = title
        self.description = description
        self.stories = list()
        self.variables = dict()

    def add_story(self, story: Story):
        self.stories.append(story)

    def remove_story(self, story: Story):
        self.stories.remove(story)
    
    def add_variable(self, var: ScenarioVariable, starting_value=None):
        self.variables[var] = starting_value
    
    def remove_variable(self, var: ScenarioVariable):
        self.variables.pop(var)

    def get_inject_by_id(self, inject_id):
        for story in self.stories:
            inject = story.get_inject_by_id(inject_id)
            if inject:
                return inject
        return None, None
