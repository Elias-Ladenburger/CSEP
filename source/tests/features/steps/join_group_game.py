from behave import *

use_step_matcher("re")


@given("an open group game")
def step_impl(context):
    raise NotImplementedError(u'STEP: Given an open group game')


@when("a participant wants to join")
def step_impl(context):
    raise NotImplementedError(u'STEP: When a participant wants to join')


@then("they enter the game lobby")
def step_impl(context):
    raise NotImplementedError(u'STEP: Then they enter the game lobby')


@given("a closed group game")
def step_impl(context):
    raise NotImplementedError(u'STEP: Given a closed group game')


@when("a participants wants to join")
def step_impl(context):
    raise NotImplementedError(u'STEP: When a participants wants to join')


@then("the participant receives an error message")
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the participant receives an error message')


@step("the maximum number of participants has already been reached")
def step_impl(context):
    raise NotImplementedError(u'STEP: And the maximum number of participants has already been reached')


@step("the game currently has fewer participants than have started the game")
def step_impl(context):
    raise NotImplementedError(u'STEP: And the game currently has fewer participants than have started the game')


@when('the trainer select "start game"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the trainer select "start game"')