from flask import render_template

from domain_layer.scenariodesign.scenario_management import EditableScenarioRepository


def get_single_scenario(scenario_id):
    return EditableScenarioRepository.get_scenario_by_id(scenario_id)


def get_entity_details(entity, details_path):
    if isinstance(entity, dict):
        entity_dict = entity
    else:
        entity_dict = entity.dict()
    return get_scenario_element(entity_dict, details_path)


def update_scenario_element(scenario_id, element_path, new_value=None):
    """new_value: None if this value is to be deleted"""
    scenario = get_single_scenario(scenario_id)
    scenario_dict = scenario.dict()
    element_key = element_path.pop(0)
    if not element_path:
        scenario_dict[element_key] = new_value
        return scenario_dict
    else:
        scenario_dict[element_key] = update_scenario_element(scenario_id, element_path, new_value)
        return scenario_dict


def delete_scenario_element(scenario_dict, element_path):
    element_key = element_path.pop(0)
    if isinstance(scenario_dict, list):
        element_key = int(element_key)
    if not element_path:
        scenario_dict.pop(element_key)
        return scenario_dict
    else:
        tmp_dict = scenario_dict[element_key]
        scenario_dict[element_key] = delete_scenario_element(tmp_dict, element_path)
        return scenario_dict


def get_scenario_element(scenario_dict, path):
    for detail in path:
        if isinstance(scenario_dict, list) and isinstance(detail, str) and detail.isnumeric():
            scenario_dict = scenario_dict[int(detail)]
        elif isinstance(scenario_dict, dict) and detail in scenario_dict:
            scenario_dict = scenario_dict[detail]
    return scenario_dict


def tab_details(template, scenario, form, **kwargs):
    return render_template(template, scenario=scenario, form=form, **kwargs)
