import copy
import datetime

from domain.scenario_design.scenario import Scenario, ScenarioVariable


class Game:
    """A scenario that is currently being played or has been played."""
    def __init__(self, scenario: Scenario):
        self.scenario = scenario
        self.start_time = datetime.datetime.now()
        self.end_time = None
        self.is_open = True
        self.variables = copy.deepcopy(scenario.variables)

    def end_game(self):
        self.is_open = False
        self.end_time = datetime.datetime.now()

    def update_variable(self, var: ScenarioVariable, new_value):
        if var.is_value_legal(new_value):
            self.variables[var] = new_value
        else:
            raise TypeError("The new value does not match the datatype of this variable!")

    def get_visible_stats(self):
        visible_stats = []
        for var in self.variables:
            if not var.hidden:
                visible_stats.append(var)
        return visible_stats

    def get_all_stats(self):
        return self.variables

    def get_inject_by_id(self, inject_id):
        return_value = self.scenario.get_inject_by_id(inject_id)
        return return_value

    @property
    def name(self):
        return self.scenario.title

    @property
    def first_inject(self):
        return self.scenario.stories[0].entry_node

    def __str__(self):
        return_str = "Game: " + self.scenario.title
        for story in self.scenario.stories:
            return_str += "\n" + str(story)
        return return_str


class GroupGame(Game):
    pass


class SoloGame(Game):
    pass