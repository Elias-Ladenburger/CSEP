import os

import flask
from flask import Blueprint, flash, redirect, render_template, request, make_response, url_for
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename

from domain_layer.scenariodesign.injects import EditableInject
from domain_layer.scenariodesign.scenario_management import EditableScenarioRepository
from presentation_layer.controllers.scenario_design import auxiliary as aux
from presentation_layer.controllers.scenario_design.scenario_forms import InjectForm

injects_bp = Blueprint('injects', __name__,
                       template_folder='../../templates/scenario', url_prefix="/scenarios")


@injects_bp.route("<scenario_id>/injects/modal")
def get_inject_modal(scenario_id):
    scenario = aux.get_single_scenario(scenario_id)
    inject_form = InjectForm(scenario)
    return render_template('/forms/inject_modal_form.html', scenario=scenario, form=inject_form)


@injects_bp.route("/<scenario_id>/inject_details")
def get_inject_details(scenario_id):
    inject_slug = request.args.get("inject_slug", False)
    if inject_slug and inject_slug != "new":
        scenario = aux.get_single_scenario(scenario_id)
        inject = scenario.get_inject_by_slug(inject_slug)
        return render_template('/forms/inject_details.html', inject=inject, scenario_id=scenario_id)
    else:
        return make_response(404, "No inject found!")


@injects_bp.route("/<scenario_id>/edit_inject", methods=["GET"])
def get_inject_form(scenario_id):
    inject_slug = request.args.get("inject_slug", False)
    scenario = aux.get_single_scenario(scenario_id)
    if inject_slug and inject_slug != "new":
        inject = scenario.get_inject_by_slug(inject_slug)
        title = "Edit inject"
    else:
        inject = False
        title = "Add inject"
    inject_form = InjectForm(scenario, inject)
    return render_template("/forms/inject_form.html", scenario=scenario,
                           inject=inject, title=title, inject_form=inject_form)


@injects_bp.route("/<scenario_id>/injects/add", methods=["POST"])
def add_inject(scenario_id):
    scenario = aux.get_single_scenario(scenario_id)
    inject_dict = process_inject_form(scenario, CombinedMultiDict((request.files, request.form)))
    if not inject_dict:
        flash("Something went wrong!", category="failure")
    else:
        is_entry_node = inject_dict.pop("is_entry_node", False)
        preceded_by = inject_dict.pop("preceded_by", "")
        inject = EditableInject(**inject_dict)
        scenario.add_inject(inject=inject, story_index=0, preceded_by_inject=preceded_by, make_entry_node=is_entry_node)
        EditableScenarioRepository.save_scenario(scenario)
        flash("Successfully added the inject!", category="success")
    return redirect(url_for('scenarios.edit_scenario', scenario_id=scenario_id) + "#" + injects_bp.name)


@injects_bp.route("/<scenario_id>/injects/update", methods=["POST", "PUT"])
def save_inject(scenario_id):
    scenario = aux.get_single_scenario(scenario_id)
    inject_dict = process_inject_form(scenario, CombinedMultiDict((request.files, request.form)))
    if not inject_dict:
        flash("Something went wrong!", category="failure")
    else:
        new_entry_node = inject_dict.pop("is_entry_node", False)
        if not inject_dict["media_path"] and not inject_dict.get("remove_inject", False):
            inject_dict["media_path"] = scenario.get_inject_by_slug(inject_dict["slug"]).media_path
        inject = EditableInject(**inject_dict)
        scenario.update_inject(inject, 0, new_entry_node)
        EditableScenarioRepository.save_scenario(scenario)
        flash("Successfully updated the inject!", category="success")
    return redirect(url_for('scenarios.edit_scenario', scenario_id=scenario_id) + "#" + injects_bp.name)


def process_inject_form(scenario, form_data):
    inject_form = InjectForm(scenario=scenario,
                             formdata=form_data)
    if inject_form.validate():
        inject_dict = inject_form.data
        if inject_form.media_path.data:
            filename = secure_filename(inject_form.media_path.data.filename)
            from presentation_layer.app import app
            upload_path = app.config['UPLOAD_FOLDER']
            inject_form.media_path.data.save(os.path.join(upload_path, filename))
            inject_dict["media_path"] = filename
        if inject_form.condition.variable_name.data:
            inject_dict["condition"] = inject_form.condition.data
        inject_dict["choices"] = inject_form.get_inject_choices()
        return inject_dict
    else:
        print(inject_form.errors)
        return None


@injects_bp.route("/<scenario_id>/injects/<inject_slug>/delete", methods=["DELETE"])
def delete_inject(scenario_id, inject_slug):
    scenario = aux.get_single_scenario(scenario_id)
    scenario.remove_inject(inject_slug)
    EditableScenarioRepository.save_scenario(scenario)
    return redirect(url_for('scenarios.edit_scenario', scenario_id=scenario_id)+ "#" + injects_bp.name)
