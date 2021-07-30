from behave import given, when, then, use_step_matcher

from domain.common.injects import BaseChoiceInject, BaseInjectChoice

use_step_matcher('parse')


@given(u'one {source_title} to start from')
def source_inject(context, source_title):
    context.source_inject = BaseChoiceInject(label=source_title, text="This is the source inject")


@given(u'a choice to go to one {target_title}')
def target_inject(context, target_title):
    context.target_inject = BaseChoiceInject(label=target_title, text="This is the target inject")
    inject_choice = BaseInjectChoice(label="A choice")
    context.source_inject.add_choice(choice)
    return target_inject


@when(u'the player selects choice at index {choice_id:d}')
def choice(context, choice_id):
    source = context.source_inject
    context.chosen_transition = source.transitions[choice_id]
    return context.chosen_transition


@then(u'this choice must refer to the {valid_title}.')
def is_choice_other(context, valid_title):
    chosen_inject = context.chosen_transition.to_inject
    assert chosen_inject.title == valid_title


@then(u'this must throw an {errortype} error.')
def step_impl(context, errortype):
    if errortype == "value":
        assert ValueError
    elif errortype == "Type":
        assert TypeError
    elif errortype == "":
        assert Exception
    else:
        assert False
