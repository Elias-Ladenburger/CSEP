from unittest import TestCase

from domain_layer.gameplay.injects import GameInject, GameInjectCondition
from domain_layer.gameplay.mock_interface import MockGameProvider



class GameTest(TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.game = MockGameProvider().get_branching_game()

    def test_game_start(self):
        self.game.start_game()
        self.assertIsInstance(self.game.current_inject, GameInject)
        print(self.game.current_inject)

    def test_game_end(self):
        self.game.end_game()

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

    def test_add_inject_history(self):
        self.game._add_inject_history("introduction", "continue")
        print(self.game.history)

    def _evaluate_change(self, change: GameVariableChange):
        """Evaluate the conditions and variable changes of a given transition.

        :param change: the Transition to evaluate.
        :return: The Inject which this transition points to.
        """
        var_name = change.var.name
        old_value = self.game_variables[var_name]
        self.game_variables[var_name].value = change.calculate_new_value(old_value)

    def test_evaluate_next_inject(self):
        pass

    def test_evaluate_next_inject_condition(self):
        alternative_inject = self.game.scenario.get_inject_by_slug("almost-done")
        condition = GameInjectCondition(alternative_inject="almost-done", comparison_operator=">",
                                        variable_name="Budget", variable_threshold=20000)
        inject = GameInject(condition=condition, label="new-inject", )

    def test_evaluate_next_inject_storyend(self):
        next_inject = self.game._evaluate_next_inject(None)
        self.assertTrue(next_inject is None)

    def test_begin_next_story(self):
        cur_story = self.game.current_story
        next_story = self.game._begin_next_story()
        self.assertTrue(cur_story is not self.game.current_story)

    def test_end_game(self):
        self.game.end_game()
        self.assertTrue(self.game.is_closed)

    def test_dict(self):
        game_dict = self.game.dict()
        print(game_dict)
        self.assertIsInstance(game_dict, dict)