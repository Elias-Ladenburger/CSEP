import os

from flask import Blueprint, flash, redirect, render_template, request, make_response, url_for, Response
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename

from application_layer.m2m_transformation import InjectChoiceTransformer, InjectTransformer
from domain_layer.scenariodesign.injects import EditableInject, InjectCondition, InjectChoice
from domain_layer.scenariodesign.scenario_management import EditableScenarioRepository
from presentation_layer.controllers.scenario_design import auxiliary as aux
from presentation_layer.controllers.scenario_design.scenario_forms import InjectForm, InjectConditionForm, \
    InjectChoicesForm

injects_bp = Blueprint('injects', __name__,
                       template_folder='../../templates/scenario', url_prefix="/scenarios")


@injects_bp.route("<scenario_id>/injects")
def edit_injects(scenario_id):
    return get_inject_page(scenario_id)


@injects_bp.route("<scenario_id>/injects/<inject_slug>")
def edit_inject(scenario_id, inject_slug):
    scenario = aux.get_single_scenario(scenario_id)
    injects = scenario.get_all_injects()
    inject = scenario.get_inject_by_slug(inject_slug)
    nodes, edges = InjectTransformer.transform_injects_to_visjs(injects)
    inject_form = InjectForm(scenario)
    return render_template("tab_injects.html", scenario=scenario, inject_form=inject_form,
                           graphnodes=nodes, graphedges=edges, active_tab="injects")


def get_inject_page(scenario_id, inject=None):
    scenario = aux.get_single_scenario(scenario_id)
    injects = scenario.get_all_injects()
    nodes, edges = InjectTransformer.transform_injects_to_visjs(injects)
    inject_form = InjectForm(scenario)
    return render_template("tab_injects.html", scenario=scenario, inject_form=inject_form, inject=inject,
                           graphnodes=nodes, graphedges=edges, active_tab="injects")


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
        return render_template('/forms/inject_details.html', inject=inject, scenario=scenario)
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
    return redirect(url_for('injects.edit_injects', scenario_id=scenario_id))


@injects_bp.route("/<scenario_id>/injects/update", methods=["POST", "PUT"])
def save_inject(scenario_id):
    scenario = aux.get_single_scenario(scenario_id)
    inject_dict = process_inject_form(scenario, CombinedMultiDict((request.files, request.form)))
    if not inject_dict:
        flash("Something went wrong!", category="failure")
    else:
        new_entry_node = inject_dict.pop("is_entry_node", False)
        remove_image = inject_dict.get("remove_image", False)
        if not inject_dict["media_path"] and not remove_image:
            inject_dict["media_path"] = scenario.get_inject_by_slug(inject_dict["slug"]).media_path
        inject = EditableInject(**inject_dict)
        scenario.update_inject(inject, 0, new_entry_node)
        EditableScenarioRepository.save_scenario(scenario)
        flash("Successfully updated the inject!", category="success")
    return redirect(url_for('injects.edit_injects', scenario_id=scenario_id))


@injects_bp.route("/<scenario_id>/injects/<inject_slug>/core", methods=["GET", "POST"])
def inject_core_form(scenario_id, inject_slug):
    scenario = aux.get_single_scenario(scenario_id)
    inject = scenario.get_inject_by_slug(inject_slug)
    inject_form = InjectForm(scenario=scenario)
    if request.method == "GET":
        inject_form.initialize(scenario=scenario, inject=inject)
    elif inject_form.validate_on_submit():
        new_entries = inject_form.data
        remove_image = new_entries.get("remove_image", False)
        if not inject_form.media_path.data and not remove_image:
            new_entries["media_path"] = inject.media_path
        if inject_form.media_path.data:
            filename = secure_filename(inject_form.media_path.data.filename)
            from presentation_layer.app import app
            upload_path = app.config['UPLOAD_FOLDER']
            inject_form.media_path.data.save(os.path.join(upload_path, filename))
            new_entries["media_path"] = filename
        inject_data = inject.dict()
        inject_data.update(new_entries)
        inject = EditableInject(**inject_data)
        scenario.update_inject(inject)
        EditableScenarioRepository.save_scenario(scenario)
        flash("Successfully updated the inject!", category="success")
    else:
        print(inject_form.errors)
        inject_form = InjectForm(scenario=scenario, inject=inject)
    return render_template("/forms/inject_core_form.html", inject_form=inject_form,
                           inject=inject, scenario=scenario)


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
        return inject_dict
    else:
        print(inject_form.errors)
        return None


@injects_bp.route("/<scenario_id>/injects/<inject_slug>/condition", methods=["GET", "POST", "DELETE"])
def inject_condition_form(scenario_id, inject_slug):
    scenario = aux.get_single_scenario(scenario_id)
    inject = scenario.get_inject_by_slug(inject_slug)
    condition_form = InjectConditionForm(scenario=scenario)
    if request.method == "GET":
        condition_form.initialize(scenario=scenario, inject=inject)
    elif request.method == "POST":
        if condition_form.validate_on_submit():
            condition_data = condition_form.data
            inject.condition = InjectCondition(**condition_data)
            scenario.update_inject(inject)
            EditableScenarioRepository.save_scenario(scenario)
            flash("Successfully updated the condition!", category="success")
        else:
            flash("Something went wrong!", category="failure")
            print(condition_form.data)
            print(condition_form.errors)
    elif request.method == "DELETE":
        inject.condition = None
        scenario.update_inject(inject)
        EditableScenarioRepository.save_scenario(scenario)
        return Response("successfully deleted the condition!", status=200)
    return render_template("/forms/inject_condition_form.html", condition_form=condition_form,
                           inject=inject, scenario=scenario)


@injects_bp.route("/<scenario_id>/injects/<inject_slug>/choices", methods=["GET", "POST"])
def inject_choices_form(scenario_id, inject_slug):
    scenario = aux.get_single_scenario(scenario_id)
    inject = scenario.get_inject_by_slug(inject_slug)
    choices_form = InjectChoicesForm(scenario)
    if request.method == "GET":
        choices_form.populate(inject=inject)
    elif request.method == "POST":
        if choices_form.validate_on_submit():
            inject.choices = []
            for choice_entry in choices_form.choice_forms.entries:
                choice_data = choice_entry.data
                inject_choice = InjectChoiceTransformer.transform_choice_data(choice_data, scenario)
                inject.choices.append(inject_choice)
            scenario.update_inject(inject)
            EditableScenarioRepository.save_scenario(scenario)
            choices_form.initialize()
            flash("Successfully updated choices!", category="success")
        else:
            flash("Something went wrong!", category="failure")
            print(choices_form.errors)
            print(choices_form.data)
    choices_form.add_option()
    return render_template("/forms/inject_choices_form.html", choices_form=choices_form,
                           inject=inject, scenario=scenario)


@injects_bp.route("/<scenario_id>/injects/<inject_slug>/choices/<choice_index>", methods=["DELETE"])
def delete_choice(scenario_id, inject_slug, choice_index):
    scenario = aux.get_single_scenario(scenario_id=scenario_id)
    inject = scenario.get_inject_by_slug(inject_slug)
    if isinstance(choice_index, str) and choice_index.isnumeric:
        choice_index = int(choice_index)
    if isinstance(choice_index, int):
        if inject.choices and -1 < choice_index < len(inject.choices):
            deleted_choice = inject.choices.pop(choice_index)
            scenario.update_inject(inject)
            EditableScenarioRepository.save_scenario(scenario)
            flash("Successfully deleted choice {}!".format(deleted_choice.label), category="success")
            return redirect(url_for('injects.inject_choices_form', scenario_id=scenario_id, inject_slug=inject_slug))
        else:
            flash("Failed to find a choice at this index: {}".format(choice_index), category="failure")
    return redirect(url_for('injects.inject_choices_form', scenario_id=scenario_id, inject_slug=inject_slug))


@injects_bp.route("<scenario_id>/injects/<inject_slug>/choices/<choice_index>/var_changes/<var_change_index>",
                  methods=["DELETE"])
def delete_variable_change(scenario_id, inject_slug, choice_index, var_change_index):
    scenario = aux.get_single_scenario(scenario_id=scenario_id)
    inject = scenario.get_inject_by_slug(inject_slug)
    inject.choices[choice_index].outcome.variable_changes.pop(var_change_index)
    scenario.update_inject(inject)
    EditableScenarioRepository.save_scenario(scenario)
    return Response("successfully deleted the variable change!", status=200)


@injects_bp.route("/<scenario_id>/injects/<inject_slug>/delete", methods=["DELETE"])
def delete_inject(scenario_id, inject_slug):
    scenario = aux.get_single_scenario(scenario_id)
    scenario.remove_inject(inject_slug)
    EditableScenarioRepository.save_scenario(scenario)
    return Response("successfully deleted the inject!", status=200)
