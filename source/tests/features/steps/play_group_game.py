from behave import *

use_step_matcher("parse")


@given('a group game in progress')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given a group game in progress')


@given(u'{participant_count} participants')
def step_impl(context, participant_count):
    raise NotImplementedError(u'STEP: Given 3 participants')


@then("the participant cannot solve another inject")
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the participant cannot solve another inject')


@given("all participants see the same inject")
def step_impl(context):
    raise NotImplementedError(u'STEP: Given all participants see the same inject')


@when("one participant solves an inject")
def step_impl(context):
    raise NotImplementedError(u'STEP: When one participant solves an inject')


@then("all participants see the same inject")
def step_impl(context):
    raise NotImplementedError(u'STEP: Then all participants see the same inject')