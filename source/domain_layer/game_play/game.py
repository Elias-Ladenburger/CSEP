import copy
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict

from pydantic import BaseModel

from domain_layer.common.auxiliary import BaseVariableChange
from domain_layer.common.injects import BaseChoiceInject
from domain_layer.common.scenarios import BaseScenario, BaseStory
from domain_layer.game_play.injects import Inject
from domain_layer.scenario_design.scenarios import EditableScenario, BaseScenarioVariable


class GameState(Enum):
    Open = 1
    In_Progress = 2
    Closed = 3


class Story(BaseStory):
    def solve_inject(self, inject_slug: str, solution):
        """
        Solves an inject with the given solution.
        Returns the next inject, if one exists.

        :param solution: The solution to this inject. Can be either a string or a Transition or a number.
        :param inject_slug: The slug of the inject that has been solved.
        :return: A transition that points to the next inject. Returns None if there is no next inject.
        """
        inject = self.get_inject_by_slug(inject_slug=inject_slug)
        return inject.solve(solution)


class GameVariableChange(BaseVariableChange):
    def calculate_new_value(self, old_value):
        operator = self.get_operator(self.operator)
        return operator(old_value, self._new_value)


class Game(BaseModel):
    """A scenario_design that is currently being played or has been played."""
    _start_time: datetime.now()
    _end_time: Optional[datetime] = None
    _game_state: GameState = GameState.Open
    _current_story_index: int = 0
    _history = []
    scenario: BaseScenario
    variables: Dict[str, BaseScenarioVariable] = {}

    def __init__(self, scenario: BaseScenario, **kwargs):
        super().__init__(scenario=scenario, **kwargs)
        self.variables = copy.deepcopy(self.scenario.variables)

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
        return self.scenario.stories[self._current_story_index]

    def start_game(self):
        self._game_state = GameState.In_Progress
        return self.scenario.stories[0].entry_node

    def set_game_variable(self, var: BaseScenarioVariable, new_value):
        self.variables[var.name].value = new_value

    def get_visible_vars(self):
        visible_stats = {}
        for var_name in self.variables:
            if self.variables[var_name].is_private:
                visible_stats[var_name] = self.variables[var_name]
        return visible_stats

    def get_all_vars(self):
        return self.variables

    def get_inject(self, inject_candidate):
        """Get an inject object that comes closest to the inject candidate."""
        if isinstance(inject_candidate, str):
            return self.get_inject_by_slug(inject_candidate)
        elif isinstance(inject_candidate, BaseChoiceInject):
            return inject_candidate
        else:
            raise TypeError("the parameter must be of type 'str' or 'Inject'!")

    def get_inject_by_slug(self, inject_slug: str):
        """Provide an inject that has the given slug."""
        inject = self.current_story.get_inject_by_slug(inject_slug)
        if not inject:
            inject = self.scenario.get_inject_by_slug(inject_slug=inject_slug)
        return inject

    def solve_inject(self, inject_candidate, solution):
        """Evaluates a solution to a given inject and provides the next inject in response.
        Side effects include appending the solution to the game history and ending the game, if no more injects exist.

        :param inject_candidate: The inject to be solved. Can be either the slug (as str)
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

    def _evaluate_change(self, change: GameVariableChange):
        """Evaluate the conditions and variable changes of a given transition.

        :param change: the Transition to evaluate.
        :return: The Inject which this transition points to.
        """
        var_name = change.var.name
        old_value = self.variables[var_name]
        self.variables[var_name].value = change.calculate_new_value(old_value)

    def _evaluate_next_inject(self, inject: Inject):
        if not inject:
            return self._begin_next_story()
        if inject.condition:
            return inject.condition.evaluate_condition(self.variables)
        else:
            return inject

    def _begin_next_story(self):
        self._current_story_index += 1
        if -1 < self._current_story_index < len(self.scenario.stories):
            return self.scenario.stories[self._current_story_index].entry_node
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
    def __init__(self, scenario: EditableScenario):
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
    def create_singleplayer_game(scenario: EditableScenario):
        game = Game(scenario=scenario)
        # GameRepository.save_game(game)
        return game

    @staticmethod
    def create_multiplayer_game(scenario: EditableScenario):
        return GroupGame(scenario)


class GameRepository:
    @staticmethod
    def save_game(game: Game):
        db = CustomDatabase()
        db.insert_one("games", game)
