from behave import *

use_step_matcher("re")


@when("the trainer selects a scenario_design")
def step_impl(context):
    raise NotImplementedError(u'STEP: When the trainer selects a scenario_design')


@step('selects "open group gameplay"')
def step_impl(context):
    raise NotImplementedError(u'STEP: And selects "open group gameplay"')


@then("the trainer should see the lobby of the new gameplay\.")
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the trainer should see the lobby of the new gameplay.')