import itertools
import random
from time import time


class GraphElement:
    """Any element within a graph"""

    id_iter = itertools.count()

    def __init__(self, label: str, elem_id=None):
        self._hash = hash(time() + random.randint(0, 100000))
        self.label = label or self._hash
        self._id = elem_id or next(self.id_iter)

    @property
    def id(self):
        return self._id

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self._hash == other._hash:
                return True
        return False

    def __repr__(self):
        return self.label

    def __str__(self):
        return self.label


class GraphNode(GraphElement):
    """The node of a graph"""
    def __init__(self, label: str, node_id=None):
        super().__init__(label=label, elem_id=node_id)


class GraphEdge(GraphElement):
    """The edge of a graph"""
    def __init__(self, source_node: GraphNode, target_node: GraphNode, label: str = "", edge_id=None):
        super().__init__(label, edge_id)
        self.source = source_node
        self.target = target_node

    def __str__(self):
        return_str = ""
        if self.label:
            return_str += self.label + "\n"
        else:
            return_str += "from: " + str(self.source.label) + "\n"
            return_str += "to: " + str(self.target.label) + "\n"
        return return_str
