from unittest import TestCase

from domain_layer.common.auxiliary import BaseScenarioVariable, DataType, BaseVariableChange
from domain_layer.gameplay.injects import GameVariable, GameVariableChange, GameInjectCondition
from domain_layer.gameplay.mock_interface import MockScenarioBuilder
from domain_layer.scenariodesign.injects import InjectCondition
from domain_layer.scenariodesign.scenarios import EditableStory


class VariablesTest(TestCase):
    def setUp(self) -> None:
        self.scenario = MockScenarioBuilder.build_scenario()

    def test_legal_numeric_var_creation(self):
        dummy_values = [
            dict(name="Budget", datatype=DataType.NUMBER, is_private=True, value="200000"),
            dict(name="Budget", datatype=DataType.NUMBER, is_private=True, value=200000),
            dict(name="Budget", datatype=DataType.NUMBER, is_private=False, value="200000"),
            dict(name="Budget!", datatype=DataType.NUMBER, is_private=True, value="200000"),
            dict(name="Budget", datatype=DataType.NUMBER, is_private=True, value="20.0000"),
            dict(name="Budget", datatype=DataType.NUMBER, is_private=True, value="20,0000"),
            dict(name="Budget", datatype=DataType.NUMBER, is_private=True, value="2.000.000"),
            dict(name="Budget", datatype=DataType.NUMBER, is_private=True, value="2,000,000"),
            dict(name="Budget", datatype=DataType.NUMBER, is_private=True, value=20.0000),
            dict(name="Budget", datatype=DataType.NUMBER, is_private=True, value="-200000"),
            dict(name="Budget", datatype=DataType.NUMBER, is_private=True, value=-200000),
            dict(name="Budget", datatype=DataType.NUMBER, is_private=True, value="-200.000"),
            dict(name="Budget", datatype=DataType.NUMBER, value="-200.000"),
        ]
        for dummy_var in dummy_values:
            with self.subTest(dummy_var=dummy_var):
                var = BaseScenarioVariable(**dummy_var)
                self.assertIsInstance(var, BaseScenarioVariable)

    def test_illegal_numeric_var_creation(self):
        dummy_values = [
            dict(name="Budget", datatype=DataType.NUMBER, is_private=True, value="20000!0"),
            dict(name="Budget", datatype=DataType.NUMBER, is_private=True, value="asdawasd"),
            dict(name="Budget", datatype=DataType.NUMBER, is_private=False, value=False),
            dict(name="", datatype=DataType.NUMBER, is_private=True, value="200000"),
            dict(datatype=DataType.NUMBER, is_private=True, value="20.0000"),
            dict(name="Budget", is_private=True, value="20,0000"),
            dict(name="Budget", datatype=DataType.NUMBER, is_private=True),
            dict(name="Budget", datatype=DataType.NUMBER, is_private=True, value="$$$$"),
            dict(name="Budget", datatype=DataType.NUMBER, is_private=True, value=""),
        ]
        for dummy_var in dummy_values:
            with self.subTest(dummy_var=dummy_var):
                var = BaseScenarioVariable(**dummy_var)
                self.assertIsInstance(var, BaseScenarioVariable)

    def test_legal_textual_var_creation(self):
        dummy_values = [
            dict(name="Some Text", datatype=DataType.TEXT, is_private=True, value="20000!0"),
            dict(name="Some Text", datatype=DataType.TEXT, is_private=False, value="20000!0"),
            dict(name="Some Text", datatype=DataType.TEXT, is_private=True, value=""),
            dict(name="Some Text", datatype=DataType.TEXT, is_private=True, value=" "),
            dict(name="Some Text", datatype=DataType.TEXT, is_private=True, value="\n"),
            dict(name="Some Text", datatype=DataType.TEXT, is_private=True, value="SELECT * FROM tbl.data;"),
            dict(name=" ", datatype=DataType.TEXT, is_private=True, value="SELECT * FROM tbl.data;"),
            dict(name="Some Text", datatype=DataType.TEXT, is_private=True, value=False),
        ]
        for dummy_var in dummy_values:
            with self.subTest(dummy_var=dummy_var):
                var = BaseScenarioVariable(**dummy_var)
                self.assertIsInstance(var, BaseScenarioVariable)

    def test_legal_boolean_var_creation(self):
        dummy_values = [
            dict(name="Some Bool", datatype=DataType.BOOL, is_private=True, value="False"),
            dict(name="Some Bool", datatype=DataType.BOOL, is_private=True, value="false"),
            dict(name="Some Bool", datatype=DataType.BOOL, is_private=True, value=False),
            dict(name="Some Bool", datatype=DataType.BOOL, is_private=True, value="No"),
            dict(name="Some Bool", datatype=DataType.BOOL, is_private=True, value="no"),
            dict(name="Some Bool", datatype=DataType.BOOL, is_private=True, value=0),
            dict(name="Some Bool", datatype=DataType.BOOL, is_private=True, value="True"),
            dict(name="Some Bool", datatype=DataType.BOOL, is_private=True, value="true"),
            dict(name="Some Bool", datatype=DataType.BOOL, is_private=True, value=True),
            dict(name="Some Bool", datatype=DataType.BOOL, is_private=True, value="Yes"),
            dict(name="Some Bool", datatype=DataType.BOOL, is_private=True, value="yes"),
            dict(name="Some Bool", datatype=DataType.BOOL, is_private=True, value="1"),
        ]
        for dummy_var in dummy_values:
            with self.subTest(dummy_var=dummy_var):
                var = BaseScenarioVariable(**dummy_var)
                self.assertIsInstance(var, BaseScenarioVariable)

    def test_illegal_textual_var_creation(self):
        dummy_values = [
            dict(name="", datatype=DataType.TEXT, is_private=True, value="20000!0"),
            dict(name="Some Text", datatype=DataType.TEXT),
            dict(datatype=DataType.TEXT, is_private=True, value=""),
        ]
        for dummy_var in dummy_values:
            with self.subTest(dummy_var=dummy_var):
                var = BaseScenarioVariable(**dummy_var)
                self.assertIsInstance(var, BaseScenarioVariable)

    def test_bool_var_change_legal_execution(self):
        var_params = dict(name="Budget", is_private=False, datatype=DataType.BOOL, value="200000")
        test_var = GameVariable(**var_params)
        change_params = [
            (dict(var=test_var, new_value="50000", operator="-"), 150000),
            (dict(var=test_var, new_value="50000", operator="+"), 250000),
            (dict(var=test_var, new_value="50000", operator="/"), 4),
            (dict(var=test_var, new_value="2", operator="*"), 400000),
        ]
        for change_param, expected_result in change_params:
            with self.subTest(change_param=change_param, expected_result=expected_result):
                test_var = GameVariable(name="Budget", is_private=False, datatype=DataType.NUMBER, value="200000")
                change = GameVariableChange(**change_param)
                old_value = test_var.value
                new_value = change.get_new_value(old_value)
                test_var.set_value(new_value)
                self.assertTrue(test_var.value == expected_result)

    def test_bool_var_change_execution(self):
        var_params = dict(name="Some Bool", is_private=False, datatype=DataType.BOOL, value="True")
        test_var = GameVariable(**var_params)
        change_params = [
            (dict(var=test_var, new_value="False", operator="="), False),
            (dict(var=test_var, new_value="True", operator="="), True),
            (dict(var=test_var, new_value=True, operator="set"), True),
            (dict(var=test_var, new_value=False, operator="set"), False),
            (dict(var=test_var, new_value="No", operator="="), False),
            (dict(var=test_var, new_value="Yes", operator="="), True),
            (dict(var=test_var, new_value="no", operator="set"), True),
            (dict(var=test_var, new_value="yes", operator="set"), False),
        ]
        for change_param, expected_result in change_params:
            with self.subTest(change_param=change_param, expected_result=expected_result):
                test_var = GameVariable(**var_params)
                change = GameVariableChange(**change_param)
                old_value = test_var.value
                new_value = change.get_new_value(old_value)
                test_var.set_value(new_value)
                self.assertTrue(test_var.value == expected_result)

    def test_create_condition(self):
        var_params = dict(name="Budget", is_private=True, datatype=DataType.NUMBER, value="200000")
        test_var = GameVariable(**var_params)
        condition_params = [
            dict(variable_name=test_var.name, comparison_operator="<",
                                 variable_threshold="1000", alternative_inject="some-inject"),
            dict(variable_name=test_var.name, comparison_operator="<=",
                 variable_threshold="1000", alternative_inject="some-inject"),
            dict(variable_name=test_var.name, comparison_operator="==",
                 variable_threshold="1000", alternative_inject="some-inject"),
            dict(variable_name=test_var.name, comparison_operator="<",
                 variable_threshold="1000", alternative_inject="")
        ]
        for condition_param in condition_params:
            with self.subTest(condition_param=condition_param):
                condition = InjectCondition(**condition_param)
                self.assertIsInstance(condition, InjectCondition)

    def test_evaluate_condition(self):
        var_params = dict(name="Budget", is_private=True, datatype=DataType.NUMBER, value="200000")
        test_var = GameVariable(**var_params)
        condition_params = [
            dict(variable_name=test_var.name, comparison_operator="<",
                                 variable_threshold="1000", alternative_inject="some-inject")
        ]
        for condition_param in condition_params:
            with self.subTest(condition_param=condition_param):
                condition = GameInjectCondition(**condition_param)
                game_vars = dict(Budget=test_var)
                is_condition_fulfilled = condition.evaluate(game_vars)
                self.assertIsInstance(is_condition_fulfilled, bool)
