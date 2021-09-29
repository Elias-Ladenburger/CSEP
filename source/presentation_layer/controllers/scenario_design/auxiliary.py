from flask import render_template

from domain_layer.scenariodesign.scenario_management import EditableScenarioRepository


def get_single_scenario(scenario_id):
    return EditableScenarioRepository.get_scenario_by_id(scenario_id)


def get_scenario_details(scenario_id, **details):
    scenario = get_single_scenario(scenario_id)
    scenario_dict = scenario.dict()
    for detail in details:
        if isinstance(scenario_dict, list) and isinstance(detail, str) and detail.isnumeric():
            scenario_dict = scenario_dict[int(detail)]
        elif isinstance(scenario_dict, dict) and detail in scenario_dict:
            scenario_dict = scenario_dict[detail]
    return scenario_dict


def tab_details(template, scenario, form, **kwargs):
    return render_template(template, scenario=scenario, form=form, **kwargs)
