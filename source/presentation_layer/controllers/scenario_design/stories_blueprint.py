import flask
from flask import Blueprint, render_template, redirect, flash, url_for

from domain_layer.scenario_design.scenario_management import EditableScenarioRepository, EditableScenarioFactory
from presentation_layer.controllers.scenario_design.scenario_forms import *
from presentation_layer.controllers.scenario_design.scenario_forms import ScenarioForm

story_bp = Blueprint('stories', __name__,
                        template_folder='../../templates/scenario', url_prefix="/scenarios/stories")
