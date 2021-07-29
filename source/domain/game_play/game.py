import copy
from datetime import datetime
from enum import Enum

from domain.scenario_design.auxiliary import VariableChange
from domain.scenario_design.injects import Inject
from domain.scenario_design.scenario import Scenario, ScenarioVariable


class GameState(Enum):
    Open = 1
    In_Progress = 2
    Closed = 3


class Game:
    """A scenario_design that is currently being played or has been played."""
    def __init__(self, scenario: Scenario):
        self.scenario = scenario
        self._start_time = datetime.now()
        self._end_time = None
        self._game_state = GameState.Open

        self.current_story_index = 0
        self.variables = copy.deepcopy(scenario.variables)
        self._history = []

    @property
    def name(self):
        return self.scenario.title

    @property
    def is_open(self):
        return self._game_state == GameState.Open

    @property
    def is_in_progress(self):
        return self._game_state == GameState.In_Progress

    @property
    def end_time(self):
        return self._end_time

    @property
    def current_story(self):
        return self.scenario.stories[self.current_story_index]

    def start_game(self):
        self._game_state = GameState.In_Progress
        return self.scenario.stories[0].entry_node

    def set_game_variable(self, var: ScenarioVariable, new_value):
        if var.is_value_legal(new_value):
            self.variables[var.name].update_value(new_value)
        else:
            raise TypeError("The new value does not match the datatype of this variable!")

    def get_visible_vars(self):
        visible_stats = {}
        for var in self.variables:
            if self.variables[var].is_private:
                visible_stats[var.name] = self.variables[var.name]
        return visible_stats

    def get_all_vars(self):
        return self.variables

    def get_inject(self, inject_candidate):
        """Get an inject object that comes closest to the inject candidate."""
        if isinstance(inject_candidate, str):
            return self.get_inject_by_slug(inject_candidate)
        elif isinstance(inject_candidate, Inject):
            return inject_candidate
        else:
            raise TypeError("the parameter must be of type 'str' or 'Inject'!")

    def get_inject_by_slug(self, inject_slug: str):
        """Provide an inject that has the given slug."""
        inject = self.current_story.get_inject_by_slug(inject_slug)
        if not inject:
            inject = self.scenario.get_inject_by_slug(inject_slug)
        return inject

    def solve_inject(self, inject_candidate, solution):
        """Evaluates a solution to a given inject and provides the next inject in response.
        Side effects include appending the solution to the game history and ending the game, if no more injects exist.

        :param inject: The inject to be solved. Can be either the slug (as str)
        of the inject or an instance of Inject itself.
        :param solution: The solution to be passed. Implementation will vary, depending on inject type.
        :return: The next inject if one exists. Otherwise returns 'None' and ends the game."""
        inject = self.get_inject(inject_candidate)
        self._add_inject_history(inject, solution)
        inject_result = self.current_story.solve_inject(inject.slug, solution)
        for var_change in inject_result.variable_changes:
            self._evaluate_change(var_change)
        return self._evaluate_next_inject(inject_result.next_inject)

    def _add_inject_history(self, inject, solution):
        history = {"inject_slug": inject.slug, "end_time": datetime.now(), "solution": solution}
        self._history.append(history)

    def _evaluate_change(self, change: VariableChange):
        """Evaluate the conditions and variable changes of a given transition.

        :param change: the Transition to evaluate.
        :return: The Inject which this transition points to.
        """
        var_name = change.var.name
        self.variables[var_name].update_value(change)

    def _evaluate_next_inject(self, inject: Inject):
        if not inject:
            return self._begin_next_story()
        if inject.condition:
            return inject.condition.evaluate_condition(self.variables)
        else:
            return inject

    def _begin_next_story(self):
        self.current_story_index += 1
        if -1 < self.current_story_index < len(self.scenario.stories):
            return self.scenario.stories[self.current_story_index].entry_node
        else:
            self.end_game()
            return None

    def end_game(self):
        self._game_state = GameState.Closed
        self._end_time = datetime.now()

    def __str__(self):
        return_str = "Game: " + self.scenario.title
        for story in self.scenario.stories:
            return_str += "\n" + str(story)
        return return_str


class GroupGame(Game):
    def __init__(self, scenario: Scenario):
        super().__init__(scenario)
        self.breakpoints = []
        self.participants = []
        self._trainers = []
        self.observers = []

    @property
    def trainer(self):
        return self._trainers

    def add_breakpoint(self, story_index):
        """
        Add a breakpoint which prevents players from moving past a specific story.
        :param story_index: The index of the story which players cannot move past.
        :return:
        """
        self.breakpoints.append(story_index)

    def remove_breakpoint(self, story_index):
        self.breakpoints.remove(story_index)


class GameFactory:
    @staticmethod
    def create_singleplayer_game(scenario: Scenario):
        game = Game(scenario)
        # GameRepository.save_game(game)
        return game

    @staticmethod
    def create_multiplayer_game(scenario: Scenario):
        return GroupGame(scenario)


class GameRepository:
    @staticmethod
    def save_game(game: Game):
        db = CustomDatabase()
        db.insert_one("games", game)
