from flask import Blueprint, render_template, redirect, url_for, request

from domain.game_play.mock_interface import MockGameProvider
game_provider = MockGameProvider()


game_gp = Blueprint('games', __name__,
                        template_folder='templates/game', url_prefix="/games")

@game_gp.route("/")
def find_game():
    game_id = request.args.get("game_id", -1)
    if game_id:
        if int(game_id) > 0:
            return redirect(url_for('games.game_start', game_id=game_id))
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
    game = game_provider.get_game()
    return render_template(template_name, scenario_name=game.name, game_id=game_id)

@game_gp.route("/<game_id>/stats")
def stats_page(game_id):
    template_name = "stats_page.html"
    game = game_provider.get_game()
    inject_id = request.args.get("inject_id", 1)
    if isinstance(inject_id, int):
        inject_id = int(inject_id)
    return render_template(template_name, scenario_name=game.name, game_id=game_id,
                           next_inject_id=inject_id, game_variables=game.variables)

@game_gp.route("/<game_id>/end")
def game_end(game_id):
    template_name = "game_end.html"
    game = game_provider.get_game()
    return render_template(template_name, scenario_name=game.name, game_id=game_id)

@game_gp.route("/<game_id>/reflection")
def game_reflection(game_id: int):
    template_name = "game_reflection.html"
    game = game_provider.get_game()
    game.end_game()
    return render_template(template_name, scenario_name=game.name, game_id=game_id)

@game_gp.route("/<game_id>/injects/<inject_id>/show")
def inject_page(game_id: int, inject_id: int):
    game = game_provider.get_game()
    inject = game.get_inject_by_id(inject_id=int(inject_id))
    template_name = "choice_inject.html"
    return render_template(template_name, scenario_name=game.name, game_id=game_id, inject_id=inject_id)

@game_gp.route("/<game_id>/injects/<inject_id>/feedback")
def inject_feedback(game_id: int, inject_id: int):
    template_name = "feedback_statistics.html"
    return render_template(template_name, scenario_name="Going Phishing",  game_id=game_id,
                           next_inject_id=(int(inject_id)+1))

@game_gp.route("/<game_id>/injects/<inject_id>/feedback_wordcloud")
def inject_wordcloud(game_id: int, inject_id: int):
    template_name = "feedback_wordcloud.html"
    return render_template(template_name, scenario_name="Going Phishing",  game_id=game_id,
                           next_inject_id=(int(inject_id) + 1))
