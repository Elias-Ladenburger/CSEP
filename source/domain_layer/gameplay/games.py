import copy
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict

from pydantic import BaseModel, PrivateAttr

from domain_layer.common._domain_objects import AggregateRoot
from domain_layer.common.auxiliary import BaseVariableChange
from domain_layer.common.injects import BaseChoiceInject
from domain_layer.common.scenarios import BaseScenario, BaseStory
from domain_layer.gameplay.injects import GameInject
from domain_layer.gameplay.participants import GameParticipant
from domain_layer.scenariodesign.scenarios import BaseScenarioVariable


class GameState(Enum):
    Open = "open"
    In_Progress = "in progress"
    Closed = "closed"
    Finished = "finished"


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


class Game(AggregateRoot):
    """A scenario that is currently being played or has been played."""
    _start_time: Optional[datetime] = PrivateAttr(None)
    _end_time: Optional[datetime] = PrivateAttr(None)
    _game_state: GameState = PrivateAttr(GameState.Open)
    _current_story_index: int = PrivateAttr(0)
    _current_inject_slug: str = PrivateAttr("")
    _history: List[InjectHistory] = PrivateAttr([])
    _type: str = "GAME"
    scenario: GameScenario
    game_variables: Dict[str, BaseScenarioVariable] = {}

    def __init__(self, scenario: GameScenario, **kwargs):
        super().__init__(scenario=scenario, **kwargs)
        self.game_variables = copy.deepcopy(self.scenario.variables)
        self._entity_id = kwargs.get("game_id")
        self._start_time = kwargs.get("start_time", datetime.now())
        self._end_time = kwargs.get("end_time", None)
        self._game_state = GameState(kwargs.get("game_state", "open"))
        self._current_story_index = kwargs.get("current_story_index", 0)
        self._current_inject_slug = kwargs.get("current_inject", "")

    @property
    def game_id(self):
        return self._entity_id

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

    @property
    def current_inject(self):
        inject = self.current_story.get_inject_by_slug(self._current_inject_slug) or self.current_story.entry_node
        return inject

    def start_game(self):
        """Begin the actual game and prepare to show the inject."""
        self._game_state = GameState.In_Progress
        self._current_story_index = 0
        self._current_inject_slug = self.current_story.entry_node.slug

    def close_game(self):
        self._game_state = GameState.Closed
        self._end_time = datetime.now()

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
        history = InjectHistory(inject_slug=inject.slug, end_time=datetime.now(), solution=solution)
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
            inject = self._begin_next_story()
        if inject.condition:
            inject = inject.condition.evaluate(self.game_variables)
        self._current_inject_slug = inject.slug
        return self.current_inject

    def _begin_next_story(self):
        """Begin the next story and return the first inject from that story.
        :returns: the first inject of the next story if one exists, None otherwise."""
        self._current_story_index += 1
        if -1 < self._current_story_index < len(self.scenario.stories):
            return self.scenario.stories[self._current_story_index].entry_node
        else:
            self.end_game()
            return None

    def end_game(self):
        self._game_state = GameState.Finished
        self._end_time = datetime.now()

    def dict(self, **kwargs):
        kwargs["by_alias"] = True
        return_dict = super().dict(**kwargs)
        return_dict.update(
            {"start_time": self._start_time,
             "end_time": self._end_time,
             "game_state": self._game_state.value,
             "current_story_index": self._current_story_index,
             "current_inject": self._current_inject_slug,
             "history": self._history,
             "type": self._type,
             "scenario_id": self.scenario.scenario_id})
        return_dict.pop("scenario")
        return return_dict

    def __str__(self):
        return_str = "Game: " + self.scenario.title
        for story in self.scenario.stories:
            return_str += "\n" + str(story)
        return return_str


class GroupGame(Game):
    breakpoints: List[str] = []
    participants: List[GameParticipant] = []
    _type: str = "GROUP_GAME"

    def __init__(self, scenario: GameScenario, **kwargs):
        super().__init__(scenario, **kwargs)

    def add_breakpoint(self, inject_slug: str):
        """
        Add a breakpoint which prevents players from moving past a specific story.
        :param inject_slug: The index of the story which players cannot move past.
        :return:
        """
        self.breakpoints.append(inject_slug)

    def remove_breakpoint(self, inject_slug: str):
        self.breakpoints.remove(inject_slug)
