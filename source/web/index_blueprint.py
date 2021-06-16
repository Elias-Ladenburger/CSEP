from flask import Blueprint, render_template
from flask_user import roles_required

from domain.game_play.mock_interface import MockGameProvider

game_provider = MockGameProvider()

index_gp = Blueprint('index', __name__,
                     template_folder='templates', url_prefix="/")


@index_gp.route("/")
def index():
    return render_template("index.html")


@index_gp.route("/login")
def login():
    return render_template("login.html")


@index_gp.route("/register")
def register():
    return render_template("signup.html")


@index_gp.route("/concept")
def concept_page():
    return render_template("concept.html")


@index_gp.route("/scenarios")
@roles_required('Admin')
def scenarios_page():
    return render_template("index.html")
