import copy
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict

from pydantic import BaseModel, PrivateAttr

from domain_layer.common.auxiliary import BaseVariableChange
from domain_layer.common.injects import BaseChoiceInject
from domain_layer.common.scenarios import BaseScenario, BaseStory
from domain_layer.gameplay.injects import GameInject
from domain_layer.gameplay.participants import GameParticipant
from domain_layer.scenariodesign.scenarios import BaseScenarioVariable


class GameState(Enum):
    Open = 1
    In_Progress = 2
    Closed = 3


class GameStory(BaseStory):
    injects: Optional[Dict[str, GameInject]] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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


class GameScenario(BaseScenario):
    stories: List[GameStory] = []


class GameVariableChange(BaseVariableChange):
    def calculate_new_value(self, old_value):
        operator = self.get_operator(self.operator)
        return operator(old_value, self._new_value)


class InjectHistory(BaseModel):
    inject_slug: str
    timestamp: datetime = datetime.now()
    solution: str

    class Config:
        allow_mutation = False


class GameHistory(BaseModel):
    _inject_history: List[InjectHistory] = PrivateAttr([])

    def append_solution(self, history: InjectHistory):
        self._inject_history.append(history)

    @property
    def inject_history(self):
        return self._inject_history


class Game(BaseModel):
    """A scenario that is currently being played or has been played."""
    _start_time: datetime = PrivateAttr(datetime.now())
    _end_time: Optional[datetime] = PrivateAttr(None)
    _game_state: GameState = PrivateAttr(GameState.Open)
    _current_story_index: int = PrivateAttr(0)
    _history = []
    scenario: GameScenario
    game_variables: Dict[str, BaseScenarioVariable] = {}

    def __init__(self, scenario: BaseScenario, **kwargs):
        super().__init__(scenario=scenario, **kwargs)
        self.game_variables = copy.deepcopy(self.scenario.variables)

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
        self.game_variables[var.name].value = new_value

    def get_visible_vars(self):
        visible_stats = {}
        for var_name in self.game_variables:
            if self.game_variables[var_name].is_private:
                visible_stats[var_name] = self.game_variables[var_name]
        return visible_stats

    def get_all_vars(self):
        return self.game_variables

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
        Side effects include appending the solution to the gameplay history
        and ending the gameplay, if no more injects exist.

        :param inject_candidate: The inject to be solved. Can be either the slug (as str)
        of the inject or an instance of Inject itself.
        :param solution: The solution to be passed. Implementation will vary, depending on inject type.
        :return: The next inject if one exists. Otherwise returns 'None' and ends the gameplay."""
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
        old_value = self.game_variables[var_name]
        self.game_variables[var_name].value = change.calculate_new_value(old_value)

    def _evaluate_next_inject(self, inject: GameInject):
        if not inject:
            return self._begin_next_story()
        if inject.condition:
            return inject.condition.evaluate_condition(self.game_variables)
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
    breakpoints: List[str] = []
    participants: List[GameParticipant] = []

    def __init__(self, scenario: BaseScenario):
        super().__init__(scenario)

    def add_breakpoint(self, inject_slug: str):
        """
        Add a breakpoint which prevents players from moving past a specific story.
        :param inject_slug: The index of the story which players cannot move past.
        :return:
        """
        self.breakpoints.append(inject_slug)

    def remove_breakpoint(self, inject_slug: str):
        self.breakpoints.remove(inject_slug)
