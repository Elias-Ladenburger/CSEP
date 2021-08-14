from behave import *

use_step_matcher("re")


@step("the trainer sees all details of the gameplay")
def step_impl(context):
    raise NotImplementedError(u'STEP: And the trainer sees all details of the gameplay')