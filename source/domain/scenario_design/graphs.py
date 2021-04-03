class GraphElement:
    """A generic element of a graph"""
    def __init__(self, label: str):
        self.label = label

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.label == other.label


class GraphNode(GraphElement):
    def __init__(self, label: str):
        super().__init__(label)


class GraphEdge(GraphElement):
    """
    A directed connection between one GraphNode to another.
    """
    def __init__(self, source_node: GraphNode, target_node: GraphNode, label: str = ""):
        super().__init__(label=label)
        self._source_node = source_node
        self._target_node = target_node

    def refers_node(self, node: GraphNode):
        return (self._source_node == node) | (self._target_node == node)

    def __eq__(self, other):
        if super().__eq__(other):
            return self._source_node == other._source_node & self._target_node == other._target_node
        else:
            return False


class Graph:
    """A generic container for graphs"""
    def __init__(self):
        self.edges = []
        self.nodes = {}  # convenience accessor

    def add_edge(self, edge: GraphEdge):
        if edge not in self.edges:
            self.edges.append(edge)

    def remove_edge(self, edge: GraphEdge):
        self.edges.remove(edge)

    def remove_node(self, node: GraphNode):
        self.nodes.pop(node)
        for edge in self.edges:
            if edge.refers_node(node):
                self.remove_edge(edge)

    def get_node_by_name(self, node_name):
        if node_name in self.nodes:
            return self.nodes[node_name]
        return None

