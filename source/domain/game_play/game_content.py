import copy
from datetime import datetime

from domain.scenario_design.auxiliary import DataType
from domain.scenario_design.injects import PlainInject, Transition
from domain.scenario_design.scenario import Scenario, ScenarioVariable


class Game:
    """A scenario that is currently being played or has been played."""
    def __init__(self, scenario: Scenario):
        self.scenario = scenario
        self.start_time = datetime.now()
        self.end_time = None
        self.is_open = True
        self.current_story_index = 0
        self.variables = copy.deepcopy(scenario.variables)
        self._history = []

    def end_game(self):
        self.is_open = False
        self.end_time = datetime.now()

    def set_game_variable(self, var: ScenarioVariable, new_value):
        if var.is_value_legal(new_value):
            self.variables[var] = new_value
        else:
            raise TypeError("The new value does not match the datatype of this variable!")

    def update_game_variable(self, var: ScenarioVariable, change_value: int):
        if var.datatype == DataType.NUMBER:
            self.variables[var] += change_value
        else:
            raise TypeError("Cannot update non-numerical game variables. Please use the 'set' function instead!")

    def get_visible_stats(self):
        visible_stats = []
        for var in self.variables:
            if not var.private:
                visible_stats.append(var)
        return visible_stats

    def get_all_stats(self):
        return self.variables

    def get_inject(self, inject_candidate):
        if isinstance(inject_candidate, int):
            return self.get_inject_by_id(inject_candidate)
        elif isinstance(inject_candidate, PlainInject):
            return inject_candidate
        else:
            raise TypeError("the parameter must be of type 'int' or 'Inject'!")

    def get_inject_by_id(self, inject_id):
        return_value = self.scenario.get_inject_by_id(inject_id)
        return return_value

    def solve_inject(self, inject, solution):
        """
        This method evaluates a solution to a given inject and provides the next inject in response.
        Side effects include appending the solution to the game history and ending the game, if no more injects exist.

        :param inject: The inject to be solved. Can be either the id of the inject or an instance of Inject itself.
        :param solution: The solution to be passed. Implementation will vary, depending on inject type.
        :return: The next inject if one exists. Otherwise returns 'None' and ends the game.

        """
        inject = self.get_inject(inject)
        self._add_inject_history(inject, solution)
        transition = inject.solve(solution)
        if transition:
            return self._evaluate_transition(transition)
        else:
            return self._begin_next_story()

    def _add_inject_history(self, inject, solution):
        history = {"inject_id": inject.id, "end_time": datetime.now(), "solution": solution}
        self._history.append(history)

    def _evaluate_transition(self, transition: Transition):
        """Evaluate the conditions and variable changes of a given transition.

        :param transition: the Transition to evaluate.
        :return: The inject which this transition points to.
        """
        if transition.state_changes:
            for change in transition.state_changes:
                old_value = self.variables[change.var]
                self.variables[change.var] = change.get_new_value(old_value)
        if transition.condition:
            if transition.condition.evaluate_condition(self.variables):
                return transition.alternative_inject
        return transition.to_inject

    def _begin_next_story(self):
        self.current_story_index += 1
        if -1 < self.current_story_index < len(self.scenario.stories):
            return self.scenario.stories[self.current_story_index].entry_node
        else:
            self.end_game()
            return None

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
