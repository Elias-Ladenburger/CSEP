import copy
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict

from pydantic import BaseModel, PrivateAttr

from domain_layer.common._domain_objects import AggregateRoot
from domain_layer.common.injects import BaseChoiceInject
from domain_layer.common.scenarios import BaseScenario, BaseStory
from domain_layer.gameplay.injects import GameInject, GameVariableChange, GameInjectResult, GameVariable
from domain_layer.gameplay.participants import GameParticipant


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
    _variables: Dict[str, GameVariable] = {}

    @classmethod
    def _prepare_variables_from_dict(cls, var_dict: dict):
        if var_dict:
            for var_name, scenario_var in var_dict.items():
                if not isinstance(scenario_var, GameVariable):
                    var_dict[var_name] = GameVariable(**scenario_var)
        return var_dict


class Game(AggregateRoot):
    """A scenario that is currently being played or has been played."""
    _start_time: Optional[datetime] = PrivateAttr(None)
    _end_time: Optional[datetime] = PrivateAttr(None)
    _game_state: GameState = PrivateAttr(GameState.Open)
    _current_story_index: int = PrivateAttr(0)
    _current_inject_slug: str = PrivateAttr("")
    _type: str = "GAME"
    scenario: GameScenario
    game_variables: Dict[str, GameVariable] = {}

    def __init__(self, scenario: GameScenario, **kwargs):
        super().__init__(scenario=scenario, **kwargs)
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
    def is_closed(self):
        return self._game_state in [GameState.Closed, GameState.Finished]

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
        self.game_variables = copy.deepcopy(self.scenario.variables)

    def close_game(self):
        self._game_state = GameState.Closed
        self._end_time = datetime.now()

    def set_game_variable(self, var_name: str, new_value):
        var = self.game_variables.get(var_name, None)
        if var:
            self.game_variables[var.name].set_value(new_value)

    def get_visible_vars(self):
        visible_stats = {}
        for var_name in self.game_variables:
            if not self.game_variables[var_name].is_private:
                visible_stats[var_name] = self.game_variables[var_name]
        return visible_stats

    def get_all_vars(self):
        return self.game_variables

    def get_inject(self, inject_candidate):
        """Get an inject object that comes closest to the inject candidate."""
        if not inject_candidate:
            return None
        elif isinstance(inject_candidate, str):
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

    def _evaluate_outcome(self, inject_result: GameInjectResult):
        """Evaluate an InjectResult object, such that all effects on the game are resolved.
        :param inject_result: the result to be evaluated.
        :returns: the next inject in this game. Returns None, if this game is finished."""
        for var_change in inject_result.variable_changes:
            self._evaluate_change(var_change)
        next_inject = self._evaluate_next_inject(inject_result.next_inject)
        return next_inject

    def _evaluate_change(self, change: GameVariableChange):
        """Evaluate the conditions and variable changes of a given transition.

        :param change: the Transition to evaluate.
        :return: The Inject which this transition points to.
        """
        var_name = change.var.name
        old_value = self.game_variables[var_name]
        self.game_variables[var_name].value = change.calculate_new_value(old_value)

    def _evaluate_next_inject(self, inject: Optional[GameInject]):
        inject = self.get_inject(inject)
        if inject is None:
            inject = self._begin_next_story()
        if inject is None:
            return inject
        elif inject.condition:
            inject = inject.condition.evaluate(self.game_variables)
        self._current_inject_slug = inject.slug
        return inject

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
             "type": self._type,
             "scenario_id": self.scenario.scenario_id})
        return_dict.pop("scenario")
        return return_dict

    def __str__(self):
        return_str = "Game: " + self.scenario.title
        for story in self.scenario.stories:
            return_str += "\n" + str(story)
        return return_str


class SingleGame(Game):
    def solve_inject(self, inject_slug, solution):
        """Evaluates a solution to a given inject and provides the next inject in response.
        Side effects include appending the solution to the gameplay history
        and ending the gameplay, if no more injects exist.

        :param inject_candidate: The inject to be solved. Can be either the slug (as str)
        of the inject or an instance of Inject itself.
        :param solution: The solution to be passed. Implementation will vary, depending on inject type.
        :return: The next inject if one exists. Otherwise returns 'None' and ends the gameplay."""
        inject = self.get_inject(inject_slug)
        inject_result = self.current_story.solve_inject(inject.slug, solution)
        return self._evaluate_outcome(inject_result)


class GroupGame(Game):
    breakpoints: List[str] = []
    next_inject_allowed: bool = False
    participants: Dict[str, GameParticipant] = {}
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

    def add_participant(self, participant_hash):
        if participant_hash not in self.participants:
            participant = GameParticipant(game_id=self.game_id, participant_id=participant_hash)
            self.participants[participant_hash] = participant
        else:
            pass

    def solve_inject(self, participant_id, inject_slug, solution):
        if participant_id not in self.participants:
            self.add_participant(participant_id)
        self.participants[participant_id].solve_inject(inject_slug, solution)

    def allow_next_inject(self):
        self.next_inject_allowed = True

    def is_next_inject_allowed(self):
        if self.next_inject_allowed:
            return True
        if self._current_inject_slug in self.breakpoints:
            return False
        for participant in self.participants:
            if not self.participants[participant].has_solved(self._current_inject_slug):
                return False
        return True

    def advance_story(self):
        self.next_inject_allowed = False
        inject_slug = self._current_inject_slug
        if self.current_inject.has_choices:
            solution = self._evaluate_solution(inject_slug)
        else:
            solution = "0"
        outcome = self.current_story.solve_inject(inject_slug, solution)
        next_inject = self._evaluate_outcome(outcome)
        return next_inject

    def _evaluate_solution(self, inject_slug: str):
        solutions = {}
        max_occurrence = 0
        for participant_id, participant in self.participants.items():
            if participant.has_solved(inject_slug):
                solution = participant.get_solution(inject_slug)
                number_of_occurrence = solutions.get(solution, 0) + 1
                solutions[solution] = number_of_occurrence
                if number_of_occurrence > max_occurrence:
                    max_occurrence = number_of_occurrence
        for solution in solutions:
            if solutions[solution] == max_occurrence:
                return solution
