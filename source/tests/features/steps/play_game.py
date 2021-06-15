from behave import *

from domain.scenario_design.game import GameFactory, Game
from domain.scenario_design.injects import Inject
from domain.scenario_design.scenario import Scenario, Story

use_step_matcher("re")


@given("one scenario")
def step_impl(context):
    learning_scenario = Scenario(title="test scenario", description="test description")

    some_inject = Inject(title="Some inject", text="Some text")
    some_story = Story(title="Some Story", entry_node=some_inject)
    learning_scenario.add_story(some_story)

    context.scenario = learning_scenario
    return context.scenario


@given(u'a game in progress')
def step_impl(context):
    context.execute_steps('''
    Given one scenario
    ''')
    context.execute_steps('''
    Given one source inject to start from
    ''')
    context.source_inject = context.scenario.stories[0].entry_node
    context.game = GameFactory.create_singleplayer_game(context.scenario)


@then('the game must end.')
def step_impl(context):
    next_inject = context.game.solve_inject(context.source_inject, 0)
