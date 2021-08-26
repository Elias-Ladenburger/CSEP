from __future__ import annotations

from typing import List

from domain_layer.common.auxiliary import BaseVariableChange
from domain_layer.common.injects import BaseChoiceInject, BaseInjectChoice, BaseInjectCondition


class EditableInject(BaseChoiceInject):
    """An inject that provides methods so that it can be edited."""
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
    """An inject condition that can be edited."""
    variable_name: str
    comparison_operator: str
    variable_threshold: str
    alternative_inject: str


class InjectChoice(BaseInjectChoice):
    """An inject choice that can be edited."""
    def set_target_inject(self, inject: BaseChoiceInject):
        """Set the target of this choice."""
        self.outcome.next_inject = inject.slug

    def add_effect(self, var_change: BaseVariableChange):
        """Add an effect to this choice."""
        self.outcome.variable_changes.append(var_change)

    def remove_effect(self, var_change: BaseVariableChange):
        """Remove an effect from this choice."""
        self.outcome.variable_changes.remove(var_change)
