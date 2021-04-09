from domain.scenario_design.graphs import GraphEdge
from domain.scenario_design.injects import Inject


class Transition(GraphEdge):
    """A transition with a custom label that leads from one Inject to another."""

    def __init__(self, from_inject: Inject, to_inject: Inject, label: str=""):
        """
        :param from_inject:
        :param to_inject:
        :param label: A brief description that will be shown to a scenario_design player. Behavior for empty values is undefined at the moment.
        """
        super().__init__(label=label, source_node=from_inject, target_node=to_inject)
        self.from_inject = self._source_node  # convenience accessor
        self.to_inject = self._target_node  # convenience accessor