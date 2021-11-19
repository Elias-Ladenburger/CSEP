import copy
import string
from datetime import datetime
from enum import Enum
import random
from typing import Optional, List, Dict, Union

from pydantic import PrivateAttr

from domain_layer.common._domain_objects import AggregateRoot
from domain_layer.common.auxiliary import BaseVariableChange
from domain_layer.common.scenarios import BaseScenario, BaseStory
from domain_layer.gameplay.injects import GameInject, GameVariableChange, GameInjectResult, GameVariable
from domain_layer.gameplay.participants import GameParticipant


class GameState(Enum):
    Open = "open"
    In_Progress = "in progress"
    Aborted = "aborted"
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
    _inject_counter: Dict[str, int] = PrivateAttr({})

    def __init__(self, scenario: GameScenario, **kwargs):
        super().__init__(scenario=scenario, **kwargs)
        self._entity_id = kwargs.get("game_id")
        self._start_time = kwargs.get("start_time", datetime.now())
        self._end_time = kwargs.get("end_time", None)
        self._game_state = GameState(kwargs.get("game_state", "open"))
        self._current_story_index = kwargs.get("current_story_index", 0)
        self._current_inject_slug = kwargs.get("current_inject", "")
        self._inject_counter = kwargs.get("inject_counter", self._initialize_inject_counter())

    def _initialize_inject_counter(self):
        inject_counter = {}
        for index, story in enumerate(self.scenario.stories):
            for inject_slug in story.injects:
                #tmp_slug = str(index) + "_" + inject_slug
                tmp_slug = inject_slug
                inject_counter[tmp_slug] = 0
        return inject_counter

    @property
    def game_id(self):
        return self._entity_id

    @property
    def name(self):
        """:return: the title of the scenario that is currently being played."""
        return self.scenario.title

    @property
    def start_time(self):
        return self._start_time

    @property
    def game_state(self):
        return self._game_state

    @property
    def is_open(self):
        """determine whether this game is currently open."""
        return self._game_state == GameState.Open

    @property
    def is_in_progress(self):
        """determine whether this game is currently in progress."""
        return self._game_state == GameState.In_Progress

    @property
    def is_playable(self):
        return self._game_state in [GameState.Open, GameState.In_Progress]

    @property
    def is_closed(self):
        """determine whether this game is already closed."""
        return self._game_state in [GameState.Aborted, GameState.Finished]

    @property
    def end_time(self):
        """:return: the timestamp when this game was closed. None if it is not yet closed."""
        return self._end_time

    @property
    def current_story(self):
        """:return: the story that is currently being played. None if the game is not yet open or already closed."""
        if self._current_story_index > len(self.scenario.stories)-1:
            return None
        return self.scenario.stories[self._current_story_index]

    @property
    def current_inject(self):
        if self.current_story:
            inject = self.current_story.get_inject_by_slug(self._current_inject_slug) or self.current_story.entry_node
            return inject
        return None

    def start_game(self):
        """Begin the actual game and prepare to show the inject."""
        self._start_time = datetime.now()
        self._game_state = GameState.In_Progress
        self.game_variables = copy.deepcopy(self.scenario.variables)
        self._current_inject_slug = self.current_story.entry_node.slug
        self._current_story_index = 0
        self._inject_counter[self._current_inject_slug] += 1

    def abort_game(self):
        """Prematurely end this game."""
        self._game_state = GameState.Aborted
        self._end_time = datetime.now()

    def set_game_variable(self, var_name: str, new_value):
        """Set the value of one this game's variables to a new value."""
        var = self.game_variables.get(var_name, None)
        if var:
            self.game_variables[var.name].set_value(new_value)
            return True
        return False

    def get_visible_vars(self):
        """:return: all Game Variables that are visible to participants."""
        visible_stats = {}
        for var_name in self.game_variables:
            if not self.game_variables[var_name].is_private:
                visible_stats[var_name] = self.game_variables[var_name]
        return visible_stats

    def get_all_vars(self):
        """:return: all Game Variables, even those that are hidden to participants."""
        return self.game_variables

    def get_inject(self, inject_candidate):
        """Get an inject object that comes closest to the inject candidate."""
        if not inject_candidate:
            return None
        elif isinstance(inject_candidate, str):
            return self.get_inject_by_slug(inject_candidate)
        elif isinstance(inject_candidate, GameInject):
            return inject_candidate
        else:
            raise TypeError("the parameter must be of type 'str' or 'Inject'!")

    def get_inject_by_slug(self, inject_slug: str):
        """Provide an inject that has the given slug."""
        inject = self.current_story.get_inject_by_slug(inject_slug)
        if not inject:
            inject = self.scenario.get_inject_by_slug(inject_slug=inject_slug)
        return inject

    def _resolve_outcome(self, inject_result: GameInjectResult):
        """Evaluate an InjectResult object, such that all effects on the game are resolved.
        :param inject_result: the result to be evaluated.
        :returns: the next inject in this game. Returns None, if this game is finished."""
        self._evaluate_changes(inject_result.variable_changes)
        next_inject = self._determine_next_inject(inject_result.next_inject)
        return next_inject

    def _evaluate_changes(self, changes: List[GameVariableChange]):
        for var_change in changes:
            if not isinstance(var_change, GameVariableChange):
                if isinstance(var_change, BaseVariableChange):
                    var_change = GameVariableChange(**var_change.dict())
                elif isinstance(var_change, dict):
                    var_change = GameVariableChange(**var_change)
            self._evaluate_change(var_change)

    def _evaluate_change(self, change: GameVariableChange):
        """Evaluate the conditions and variable changes of a given transition.

        :param change: the Transition to evaluate.
        :return: The Inject which this transition points to.
        """
        var_name = change.var.name
        old_value = self.game_variables[var_name].value
        new_value = change.get_new_value(old_value)
        self.game_variables[var_name].set_value(new_value)

    def _determine_next_inject(self, inject: Optional[GameInject]) -> Union[GameInject, None]:
        """Evaluate which inject to show next.
        :return: the next inject if one exists, None otherwise."""
        inject = self.get_inject(inject)
        if not inject:
            inject = self._begin_next_story()
        if not inject:
            return inject
        elif inject.condition and inject.condition.evaluate(self.game_variables):
            inject = self.get_inject(inject.condition.alternative_inject)
        self._current_inject_slug = inject.slug
        return inject

    def _show_next_inject(self, next_inject):
        """If a next inject exists, this will be returned. Otherwise the game will end.

        :param next_inject: either an object of type GameInject or None"""
        if next_inject:
            self._inject_counter[self._current_inject_slug] += 1
            self._current_inject_slug = next_inject.slug
            return next_inject
        else:
            self.end_game()
            return next_inject

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
        """
        Finish this game. It can now no longer be played.
        """
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
             "scenario_id": self.scenario.scenario_id,
             "inject_counter": self._inject_counter})
        return_dict.pop("scenario")
        return return_dict

    def __str__(self):
        return_str = "Game: " + self.scenario.title
        for story in self.scenario.stories:
            return_str += "\n" + str(story)
        return return_str


class SingleGame(Game):
    """A game played by a single person."""
    def solve_inject(self, inject_candidate, solution):
        """Evaluates a solution to a given inject and provides the next inject in response.
        Side effects include appending the solution to the gameplay history
        and ending the gameplay, if no more injects exist.

        :param inject_candidate: The inject to be solved. Can be either the slug (as str)
        of the inject or an instance of Inject itself.
        :param solution: The solution to be passed. Implementation will vary, depending on inject type.
        :return: The next inject if one exists. Otherwise returns 'None' and ends the gameplay."""
        inject = self.get_inject(inject_candidate)
        inject_result = self.current_story.solve_inject(inject.slug, solution)
        next_inject = self._resolve_outcome(inject_result)
        return next_inject


class GroupGame(Game):
    """A Game that can be played collaboratively
    (by a group of participants who all share the same variables and injects)."""
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
        """Remove a breakpoint for a given inject."""
        self.breakpoints.remove(inject_slug)

    def add_participant(self, participant_hash: str = ""):
        """Add another participant to this game."""
        if not participant_hash:
            participant_hash = self._generate_participant_hash()
        if participant_hash not in self.participants:
            participant = GameParticipant(participant_id=participant_hash)
            if self.is_in_progress and self._inject_counter[self._current_inject_slug] >= 0:
                participant.initialize_history(self._inject_counter, self._current_inject_slug)
            self.participants[participant_hash] = participant
        return participant_hash

    def number_of_participants(self):
        """:return: how many active participants this game currently has."""
        return len(self.participants)

    def solve_inject(self, participant_id, inject_slug, solution):
        """Have a single participant submit their solution to an inject."""
        if participant_id not in self.participants:
            self.add_participant(participant_id)
        self.participants[participant_id].solve_inject(inject_slug, solution)

    def has_participant_solved(self, participant_hash: str):
        """Check whether a participant has solved the current inject."""
        participant = self.participants.get(participant_hash, False)
        if not participant:
            return False
        solved_count = participant.solved_count(self._current_inject_slug)
        return solved_count >= self._inject_counter[self._current_inject_slug]

    def allow_next_inject(self):
        """Allow advancement of the game, even if this were not possible otherwise."""
        self.next_inject_allowed = True

    def is_next_inject_allowed(self):
        """Check whether participants should be able to see and solve the next inject."""
        if self.next_inject_allowed:
            return True
        if self._current_inject_slug in self.breakpoints:
            return False
        for participant in self.participants:
            if not self.has_participant_solved(participant):
                return False
        return True

    def advance(self):
        """Returns the next inject in the story."""
        self.next_inject_allowed = False
        solution = "0"
        if self.current_inject.has_choices:
            solution = self._determine_groups_solution(self._current_inject_slug)
        outcome = self.current_story.solve_inject(self._current_inject_slug, solution)
        next_inject = self._resolve_outcome(outcome)
        return self._show_next_inject(next_inject)

    def _determine_groups_solution(self, inject_slug: str):
        """Count how often each solution to an inject has been submitted.
        :return: the most popular solution."""
        solution_occurrences = self.determine_group_answers(inject_slug)
        max_occurrence = 0
        most_popular = ""
        for solution in solution_occurrences:
            if solution_occurrences[solution] > max_occurrence:
                max_occurrence = solution_occurrences[solution]
                most_popular = solution
        return most_popular

    def determine_group_answers(self, inject_slug: str):
        """Evaluate how often each solution has occurred."""
        inject = self.get_inject(inject_slug)
        solution_occurrences = {}
        for participant_id, participant in self.participants.items():
            if participant.has_solved(inject.slug):
                solution = participant.get_solution(inject.slug)
                if inject.has_choices:
                    solution = str(inject.choices[int(solution)])
            else:
                solution = "no solution"
            number_of_occurrences = solution_occurrences.get(solution, 0) + 1
            solution_occurrences[solution] = number_of_occurrences
        return solution_occurrences

    @staticmethod
    def _generate_participant_hash():
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(10))
        return random_string