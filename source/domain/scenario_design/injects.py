from typing import List

from domain.scenario_design.auxiliary import Image
from domain.scenario_design.graphs import GraphNode, GraphEdge


class Inject(GraphNode):
    """An inject in a story"""
    def __init__(self, title: str, text: str, image: Image = None):
        super().__init__(label=title)
        self.text = text
        self.image = image or Image()
        self.inject_id = self._hash
        self._type = "Inject"

    @property
    def id(self):
        if self.inject_id:
            return self.inject_id
        else:
            return "unset ID"

    @property
    def type(self):
        return self._type

    def __str__(self):
        return_str = self.type + "\n"
        return_str += self.id + "\n" + self.label + "\n"
        return_str += self.text
        return return_str


class Transition(GraphEdge):
    """A transition with a custom label that leads from one Inject to another."""

    def __init__(self, from_inject: Inject, to_inject: Inject, label: str = ""):
        """
        :param from_inject:
        :param to_inject:
        :param label: A brief description that will be shown to a scenario_design player. Behavior for empty values is undefined at the moment.
        """
        super().__init__(label=label, source_node=from_inject, target_node=to_inject)
        self.from_inject = self.source  # convenience accessor
        self.to_inject = self.target  # convenience accessor
        self._id = id

    @property
    def id(self):
        if self._id:
            return self._id
        else:
            return None

    def __str__(self):
        return_str = ""
        if self.id:
            return_str += "Transition " + self.id + "\n"
        if self.label:
            return_str += self.label + "\n"
        return_str += "from: " + str(self.from_inject.label) + "\n"
        return_str += "to: " + str(self.to_inject.label) + "\n"
        return return_str


class InformativeInject(Inject):
    """An inject that refers to only one other inject and
    therefore serves no other purpose than to inform the player of something."""
    def __init__(self, title: str, transition: Transition, text: str, inject_id="", image: Image = None):
        super().__init__(title=title, text=text, image=image)
        self._type = "Informative Inject"

    def __str__(self):
        return_str = super().__str__()
        return_str += "\n followed by " + self.transition.to_inject.label
        return return_str


class ChoiceInject(Inject):
    """An inject that refers to more than one other inject and
        therefore requires the player to make a choice."""

    def __init__(self, title: str, transitions: List[Transition], text: str, inject_id="", image: Image = None):
        super().__init__(title=title, text=text, inject_id=inject_id, image=image)
        self._type = "Choice Inject"
        self.transitions = transitions

    def add_transition(self, transition: Transition):
        self.transitions.append(transition)

    def __str__(self):
        return_str = super().__str__()
        for transition in self.transitions:
            return_str += "\nOption " + transition.label + " points to " + transition.to_inject.label
        return return_str


class InputInject(InformativeInject):
    """An inject that requires the player to make textual input, but only refers to one other inject."""
    def __init__(self, title: str, transition: Transition, text: str, inject_id="", image: Image = None):
        super().__init__(title=title, transition=transition, text=text, inject_id=inject_id, image=image)
        self._type = "Input Inject"

