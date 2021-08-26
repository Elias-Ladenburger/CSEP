import random
from time import time
from typing import Optional

from pydantic import BaseModel


class GraphElement(BaseModel):
    """Any element within a graph"""
    label: str

    def __repr__(self):
        return self.label

    def __str__(self):
        return self.label


class GraphNode(GraphElement):
    """The node of a graph"""
    def __init__(self, label: str, **keyword_args):
        super().__init__(label=label, **keyword_args)


class GraphEdge(GraphElement):
    """The edge of a graph"""
    source_node: GraphNode
    target_node: GraphNode

    def __str__(self):
        return_str = ""
        if self.label:
            return_str += self.label + "\n"
        else:
            return_str += "from: " + str(self.source_node.label) + "\n"
            return_str += "to: " + str(self.target_node.label) + "\n"
        return return_str
