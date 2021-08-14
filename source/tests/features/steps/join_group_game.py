from behave import *

use_step_matcher("re")


@given("an open group gameplay")
def step_impl(context):
    raise NotImplementedError(u'STEP: Given an open group gameplay')


@when("a participant wants to join")
def step_impl(context):
    raise NotImplementedError(u'STEP: When a participant wants to join')


@then("they enter the gameplay lobby")
def step_impl(context):
    raise NotImplementedError(u'STEP: Then they enter the gameplay lobby')


@given("a closed group gameplay")
def step_impl(context):
    raise NotImplementedError(u'STEP: Given a closed group gameplay')


@when("a participants wants to join")
def step_impl(context):
    raise NotImplementedError(u'STEP: When a participants wants to join')


@then("the participant receives an error message")
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the participant receives an error message')


@step("the maximum number of participants has already been reached")
def step_impl(context):
    raise NotImplementedError(u'STEP: And the maximum number of participants has already been reached')


@step("the gameplay currently has fewer participants than have started the gameplay")
def step_impl(context):
    raise NotImplementedError(u'STEP: And the gameplay currently has fewer participants than have started the gameplay')


@when('the trainer select "start gameplay"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the trainer select "start gameplay"')