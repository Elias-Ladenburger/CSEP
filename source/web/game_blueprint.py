from flask import Blueprint, render_template, redirect, url_for, request

from domain.game_play.game_content import Game
from domain.scenario_design.scenario import Scenario

game_gp = Blueprint('games', __name__,
                        template_folder='templates/game', url_prefix="/games")

@game_gp.route("/")
def find_game():
    game_id = int(request.args.get("game_id", -1))
    if game_id > 0:
        return redirect(url_for('games.game_start', game_id=game_id))
    else:
        return games_page()


@game_gp.route("/singleplayer/overview")
def games_page():
    return redirect(url_for('index'))

@game_gp.route("/multiplayer/overview")
def multiplayer_overview():
    return render_template("group_overview.html")


@game_gp.route("/<game_id>")
def game_start(game_id):
    template_name = "game_start.html"
    return render_template(template_name, scenario_name="Going Phishing", game_id=game_id)

@game_gp.route("/<game_id>/stats")
def stats_page(game_id):
    template_name = "stats_page.html"
    return render_template(template_name, scenario_name="Going Phishing", game_id=game_id)

@game_gp.route("/<game_id>/end")
def game_end(game_id):
    template_name = "game_end.html"
    return render_template(template_name, scenario_name="Going Phishing", game_id=game_id)

@game_gp.route("/<game_id>/reflection")
def game_reflection(game_id):
    template_name = "game_reflection.html"
    #TODO: close game
    return render_template(template_name, scenario_name="Going Phishing", game_id=game_id)

@game_gp.route("/<game_id>/injects/<inject_id>/show")
def inject_page(game_id, inject_id):
    template_name = "choice_inject.html"
    if int(inject_id) % 2 == 0:
        template_name = "informative_inject.html"
    return render_template(template_name, scenario_name="Going Phishing", game_id=game_id)

@game_gp.route("/<game_id>/injects/<inject_id>/feedback")
def inject_feedback(game_id, inject_id):
    template_name = "feedback_view.html"
    return render_template(template_name, scenario_name="Going Phishing",  game_id=game_id, inject_id=inject_id)

