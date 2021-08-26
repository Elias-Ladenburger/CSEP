from datetime import datetime
from unittest import TestCase

from domain_layer.gameplay.games import GroupGame
from domain_layer.gameplay.injects import GameInject, GameInjectCondition
from domain_layer.gameplay.mock_interface import MockGameProvider
from domain_layer.gameplay.participants import GameParticipant


class GameTest(TestCase):
    def setUp(self) -> None:
        self.game = MockGameProvider().get_branching_game()

    def test_game_start(self):
        self.game.start_game()
        self.assertIsInstance(self.game.current_inject, GameInject)
        print(self.game.current_inject)

    def test_game_end(self):
        self.game.end_game()

    def test_start_game(self):
        pass

    def test_close_game(self):
        pass

    def test_set_game_variable(self):
        pass

    def test_get_visible_vars(self):
        pass

    def test_get_all_vars(self):
        pass

    def test_get_inject_is_slug(self):
        inject_candidate = "introduction"
        inject = self.game.get_inject(inject_candidate)
        self.assertIsInstance(inject, GameInject)
        self.assertTrue(inject.slug == inject_candidate)

    def test_get_inject_by_slug(self):
        slug = "introduction"
        inject = self.game.get_inject_by_slug(slug)
        self.assertIsInstance(inject, GameInject)
        self.assertTrue(inject.slug == slug)

    def test_group_solve_informative_inject(self):
        inject_slug = "introduction"
        participant_name = "some participant"
        scenario = self.game.scenario
        groupgame = GroupGame(scenario=scenario, **self.game.dict())

        groupgame.solve_inject(participant_name, inject_slug, "0")
        self.assertTrue(participant_name in groupgame.participants)
        self.assertTrue(groupgame.participants["some participant"].has_solved(inject_slug))

    def test_add_inject_history_to_participant(self):
        inject_slug = "introduction"
        participant = GameParticipant(game_id="some id", participant_id="some participant" )
        participant.solve_inject(inject_slug, "0")
        self.assertTrue(participant.has_solved(inject_slug))

    def test_evaluate_change(self):
        pass

    def test_evaluate_next_inject(self):
        pass

    def test_evaluate_next_inject_condition(self):
        pass

    def test_evaluate_next_inject_storyend(self):
        next_inject = self.game._determine_next_inject(None)
        self.assertTrue(next_inject is None)

    def test_begin_next_story(self):
        cur_story = self.game.current_story
        next_story = self.game._begin_next_story()
        self.assertTrue(cur_story is not self.game.current_story)

    def test_begin_last_story_ends_game(self):
        cur_story = None
        for story in self.game.scenario.stories:
            cur_story = self.game._begin_next_story()
        story_beyond_last_story = self.game._begin_next_story()
        self.assertFalse(story_beyond_last_story)

    def test_end_game_leads_to_close(self):
        self.game.end_game()
        self.assertTrue(self.game.is_closed)

    def test_end_game_saves_timestamp(self):
        current_time = datetime.now()
        self.game.end_game()
        self.assertEqual(self.game._end_time.minute, current_time.minute)

    def test_dict(self):
        game_dict = self.game.dict()
        print(game_dict)
        self.assertIsInstance(game_dict, dict)
