from __future__ import annotations

from typing import List, Optional

from pydantic import PrivateAttr

from domain_layer.common.auxiliary import BaseVariableChange
from domain_layer.common.injects import BaseChoiceInject, BaseInjectChoice, BaseInjectCondition


class EditableInject(BaseChoiceInject):
    @property
    def title(self):
        return self.label

    @title.setter
    def title(self, new_title: str):
        self.label = new_title

    def add_choices(self, new_choices: List[BaseInjectChoice]):
        for choice in new_choices:
            self.choices.append(choice)


class InjectCondition(BaseInjectCondition):
    variable_name: str
    comparison_operator: str
    variable_threshold: str
    alternative_inject: str


class InjectChoice(BaseInjectChoice):
    def set_target_inject(self, inject: BaseChoiceInject):
        self.outcome.next_inject = inject.slug

    def add_effect(self, var_change: BaseVariableChange):
        self.outcome.variable_changes.append(var_change)

    def remove_effect(self, var_change: BaseVariableChange):
        self.outcome.variable_changes.remove(var_change)