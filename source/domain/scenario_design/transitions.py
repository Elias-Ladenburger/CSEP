from domain.scenario_design.graphs import GraphEdge
from domain.scenario_design.injects import Inject


class Transition(GraphEdge):
    """A transition with a custom label that leads from one Inject to another."""

    def __init__(self, from_inject: Inject, to_inject: Inject, label: str = "", id=""):
        """
        :param from_inject:
        :param to_inject:
        :param label: A brief description that will be shown to a scenario_design player. Behavior for empty values is undefined at the moment.
        """
        super().__init__(label=label, source_node=from_inject, target_node=to_inject)
        self.from_inject = self._source_node  # convenience accessor
        self.to_inject = self._target_node  # convenience accessor
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
