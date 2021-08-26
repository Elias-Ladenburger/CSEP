from flask import Blueprint, render_template, url_for, redirect

from domain_layer.common.scenario_management import ScenarioRepository

index_gp = Blueprint('index', __name__,
                     template_folder='../../templates', url_prefix="/")


@index_gp.route("/")
def index():
    scenarios = ScenarioRepository.get_all_scenarios()
    return render_template("index.html", scenarios=scenarios)


@index_gp.route("/login")
def login():
    return render_template("login.html")


@index_gp.route("/scenarios")
def scenarios():
    return redirect(url_for("scenarios.show_scenarios"))


@index_gp.route("/register")
def register():
    return render_template("signup.html")


@index_gp.route("/concept")
def concept_page():
    return render_template("concept.html")


@index_gp.route("/scenarios")
def scenarios_page():
    return render_template("index.html")


@index_gp.route("/404")
def not_found_page():
    return render_template("404_not_found.html")
