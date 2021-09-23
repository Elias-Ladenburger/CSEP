import json
from typing import List

from domain_layer.common.auxiliary import BaseVariableChange
from domain_layer.common.injects import BaseChoiceInject, InjectResult
from domain_layer.common.scenarios import BaseStory, BaseScenario
from domain_layer.gameplay.games import GroupGame
from domain_layer.scenariodesign.injects import InjectChoice


class InjectTransformer:
    """This class transforms domain-layer injects to other datastructures."""

    @classmethod
    def transform_inject_to_visjs(cls, injects: List[BaseChoiceInject]):
        """Transform a number of injects to JSON, so that they can be used as input for the VISJS-network
         Javascript library.
        :param injects: the injects to be transformed.
        :return: a tuple of nodes and edges in JSON-format."""
        injects, edges = cls.transform_injects_to_visjs_dict(injects)
        return json.dumps(injects), json.dumps(edges)

    @classmethod
    def transform_injects_to_visjs_dict(cls, injects: List[BaseChoiceInject],
                                        group_id: int = 0, entry_node: str = ""):
        """
        Transform a number of injects to JSON, so that they can be used as input for the VISJS-network Javascript library.
        Highlights the entry node in a different color and groups injects according to group_id.
        :param injects: a list of injects to be transformed
        :param group_id: The id of this group.
        :param entry_node: The slug of the entry node of this story.
        :returns: a dictionary that represents the data structure used by vis.DataSet
        """
        inject_list = []
        edge_list = []
        level = 1
        for inject in injects:
            tmp_nodes, tmp_edges = cls._transform_inject(inject, group_id, level, entry_node)
            inject_list += [*tmp_nodes]
            edge_list += [*tmp_edges]
            level += 1
        return inject_list, edge_list

    @classmethod
    def transform_stories_to_visjs(cls, stories: List[BaseStory]):
        injects, edges = cls.transform_stories_to_visjs_dict(stories)
        return json.dumps(injects), json.dumps(edges)

    @classmethod
    def transform_stories_to_visjs_dict(cls, stories: List[BaseStory]):
        story_index = 0
        all_injects = []
        all_edges = []
        for story in stories:
            if story.entry_node:
                injects = [*story.injects.values()]
                new_injects, new_edges = \
                    cls.transform_injects_to_visjs_dict(injects, group_id=story_index, entry_node=story.entry_node.slug)
                story_index += 1
                all_injects += [*new_injects]
                all_edges += [*new_edges]
        return all_injects, all_edges

    @classmethod
    def _transform_inject(cls, inject, group_id, level, entry_node=False):
        tmp_edges = []
        tmp_nodes = []
        tmp_id = inject.slug
        if group_id > 0:
            tmp_id += str(group_id)
        x = 200 * group_id
        y = level * -200
        tmp_inject = dict(id=tmp_id, label=inject.label, text=inject.text, group=group_id, level=level, slug=inject.slug)
        if inject.slug == entry_node:
            tmp_inject["is_entry_node"] = True
        tmp_nodes.append(tmp_inject)
        if inject.next_inject:
            tmp_edges = cls._transform_edges(inject, tmp_id, group_id)
        if inject.condition:
            condition_id = tmp_id + "_condition"
            condition_title = str(inject.condition)
            tmp_condition = dict(id=condition_id, label="condition", title=condition_title, group=group_id,
                                 level=level)
            tmp_condition_edge = {"from": condition_id, "to": tmp_id, "label": "triggers before"}
            tmp_result_edge = {"from": condition_id, "to": inject.condition.alternative_inject, "label": "leads to"}
            tmp_nodes.append(tmp_condition)
            tmp_edges.append(tmp_condition_edge)
            tmp_edges.append(tmp_result_edge)
        return tmp_nodes, tmp_edges

    @classmethod
    def _transform_edges(cls, inject, tmp_id, group_id):
        next_id = inject.next_inject
        if group_id > 0:
            next_id += str(group_id)
        edge_list = []
        edge_list.append({"from": tmp_id, "to": next_id, "label": "[default]"})
        if inject.has_choices:
            for choice in inject.choices:
                title = choice.label
                outcome = choice.outcome
                if outcome.next_inject:
                    next_id = choice.outcome.next_inject
                    if group_id > 0:
                        next_id += str(group_id)
                edge_list.append({"from": tmp_id, "to": next_id, "label": choice.label, "title": title})
        return edge_list

    @classmethod
    def transform_injects_to_visjs(cls, injects):
        injects, edges = cls.transform_injects_to_visjs_dict(injects)
        return json.dumps(injects), json.dumps(edges)


class ScenarioTransformer:
    """Transform scenarios to frontend-friendly formats."""
    @staticmethod
    def scenario_as_json(scenario: BaseScenario):
        """Transform a given scenario to JSON."""
        scenario_dict = scenario.dict()
        return json.dumps(scenario_dict)

    @staticmethod
    def scenario_as_dict(scenario: BaseScenario):
        """Transform a given scenario to dict."""
        return scenario.dict()

    @staticmethod
    def scenarios_as_json(scenarios: List[BaseScenario]):
        """Transform a number of scenarios to JSON."""
        scenario_list = []
        for scenario in scenarios:
            scenario_list.append(ScenarioTransformer.scenario_as_dict(scenario))
        scenario_dict = {"scenarios": scenario_list}
        return json.dumps(scenario_dict)

    @staticmethod
    def scenarios_as_dict(scenarios: List[BaseScenario]):
        """Transform a number of scenarios to a list of dicts."""
        scenario_list = ScenarioTransformer.scenarios_as_json_list(scenarios)
        scenarios_dict = {"scenarios": scenario_list}
        return scenarios_dict

    @staticmethod
    def scenarios_as_json_list(scenarios: List[BaseScenario]):
        """Transform a number of scenarios to a list of JSONs."""
        scenario_list = []
        for scenario in scenarios:
            scenario_list.append(ScenarioTransformer.scenario_as_dict(scenario))
        return scenario_list


class SolutionTransformer:
    """A collection-class that can transform the solutions to a game inject
    into a format that can be understood by frontend-libraries."""

    @classmethod
    def transform_solution_to_canvasjs(cls, game: GroupGame, inject_slug: str):
        """
        :returns: a list of dictionaries of the format [{"y": number_of_solutions, "label": solution_label}, ...]
        """
        return_data = []  # [{"y": 5, "label": "Answer 1"}, {"y": 5, "label": "Answer 2"}]
        solution_occurrences = game.solution_occurrence(inject_slug)
        inject = game.get_inject(inject_slug)

        for solution in solution_occurrences:
            occurrence = solution_occurrences[solution]
            if isinstance(solution, int) or solution.isnumeric():
                solution = "Continue"
            return_data.append({"y": occurrence, "label": solution})
        return return_data


class VarChangeTransformer():
    @classmethod
    def transform_var_change_form(cls, var_changes_raw, scenario: BaseScenario):
        """Transform data in the form of {variable_name: str, variable_operator: str, new_value: str}
        to a VariableChange object"""
        var_change_objects = []
        for var_change_data in var_changes_raw:
            var_name = var_change_data.get("variable_name")
            operator = var_change_data.get("value_operator")
            new_val = var_change_data.get("new_value")
            var = scenario.variables.get(var_name)
            if not var:
                raise ValueError("This scenario does not have a variable called {}!".format(var_name))
            else:
                var_change = BaseVariableChange(var=var, operator=operator, new_value=new_val)
                var_change_objects.append(var_change)
        return var_change_objects


class InjectChoiceTransformer:
    @classmethod
    def transform_choices_data(cls, choices_raw_data):
        choices = []
        for choice_data in choices_raw_data:
            choice = cls.transform_choice_data(choice_data)
            choices.append(choice)
        return choices

    @classmethod
    def transform_choice_data(cls, choice_raw_data, scenario):
        label = choice_raw_data.get("choice_label")
        next_inject = choice_raw_data.get("next_inject")
        variable_changes = VarChangeTransformer.transform_var_change_form(choice_raw_data.get("variable_changes"),
                                                                          scenario=scenario)

        outcome = InjectResult(next_inject=next_inject,
                               variable_changes=variable_changes)
        inject_choice = InjectChoice(label=label, outcome=outcome)
        return inject_choice
