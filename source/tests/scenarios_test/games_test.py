import unittest

from domain.game_play.game_content import Game
from domain.scenario_design.scenario import Scenario


class InjectTest(unittest.TestCase):

    def test_play_game(self):
        scenario = Scenario()
        game = Game(scenario)
        for story in game.scenario.stories:
            self.test_play_story(story)

    def test_play_story(self, story: Story):
        story.entry_node