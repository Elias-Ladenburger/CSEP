import random
from time import time


class GraphElement:
    """Any element within a graph"""
    def __init__(self, label: str):
        self._hash = hash(time() + random.randint(0, 100000))
        self.label = label or self._hash

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self._hash == other._hash:
                return True
        return False

    def __repr__(self):
        return self.label


class GraphNode(GraphElement):
    """The node of a graph"""
    def __init__(self, label: str):
        super().__init__(label)


class GraphEdge(GraphElement):
    """The edge of a graph"""
    def __init__(self, source_node: GraphNode, target_node: GraphNode, label: str = ""):
        super().__init__(label)
        self.source = source_node
        self.target = target_node
