from typing import List

from domain.scenario.auxiliary import Image
from domain.scenario.graphs import GraphNode, GraphEdge, Graph


class Inject(GraphNode):
    """An inject in a story"""
    def __init__(self, title: str, description="", image: Image = None):
        super().__init__(title)
        if image is None:
            image = {"image_path": "", "image_position": ""}
        self.description = description
        self.image = image or Image()


class Transition(GraphEdge):
    def __init__(self, title: str, from_inject: Inject, to_inject: Inject):
        super().__init__(title, from_inject, to_inject)
        self.title = title
        self.from_inject = self._source_node  # convenience accessor
        self.to_inject = self._target_node  # convenience accessor


class StoryGraph(Graph):
    """A collection of injects and transitions within a story"""
    def __init__(self, injects=List[Inject], transitions=List[Transition]):
        super().__init__()
        self.injects = injects
        self.transitions = transitions


class Story:
    """A _Story_ is a collection of injects within a scenario"""

    def __init__(self, title: str, entry_node: Inject, exit_node: Inject, story_graph=None):
        self._title = title
        self._entry_node = entry_node
        self._exit_node = exit_node
        if story_graph:
            self._story_graph = story_graph

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if isinstance(title, str):
            self._title = title
        else:
            raise TypeError


