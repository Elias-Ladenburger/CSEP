from behave import *

from domain_layer.gameplay.games import GameFactory
from domain_layer.common.injects import BaseChoiceInject
from domain_layer.scenariodesign.scenarios import EditableScenario, BaseStory

use_step_matcher("parse")


@step("a learning scenario_design")
def step_impl(context):
    learning_scenario = EditableScenario(title="test scenario_design", description="test description")

    some_inject = BaseChoiceInject(title="Some inject", text="Some text")
    some_story = BaseStory(title="Some Story", entry_node=some_inject)
    learning_scenario.add_story(some_story)

    context.scenario = learning_scenario
    return context.scenario


@given("one scenario_design")
def step_impl(context):
    context.execute_steps("Given a learning scenario_design")


@given(u'a gameplay in progress')
def step_impl(context):
    context.execute_steps('''
    Given one scenario_design
    ''')
    context.execute_steps('''
    Given one source inject to start from
    ''')
    context.source_inject = context.scenario.stories[0].entry_node
    context.game = GameFactory.create_singleplayer_game(context.scenario)


@then('the gameplay must end.')
def step_impl(context):
    next_inject = context.game.solve_inject(context.source_inject, 0)


@given("a trainer")
def step_impl(context):
    raise NotImplementedError(u'STEP: Given a trainer')


@given("a participant that belongs to a target group")
def step_impl(context):
    raise NotImplementedError(u'STEP: Given a participant that belongs to a target group')


@step("an inject hint that is defined for this target group")
def step_impl(context):
    raise NotImplementedError(u'STEP: And an inject hint that is defined for this target group')


@when("the participant sees this inject")
def step_impl(context):
    raise NotImplementedError(u'STEP: When the participant sees this inject')


@then("the participant should see the hint")
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the participant should see the hint')