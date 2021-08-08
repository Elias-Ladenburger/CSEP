import flask
from flask import Blueprint, render_template, redirect, flash, url_for

from domain.scenario_design.scenario_management import EditableScenarioRepository, EditableScenarioFactory
from web.controllers.scenario_design.scenario_forms import *
from web.controllers.scenario_design.scenario_forms import ScenarioForm

story_bp = Blueprint('stories', __name__,
                        template_folder='../../templates/scenario', url_prefix="/scenarios/stories")
