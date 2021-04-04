from flask import Blueprint, render_template

game_gp = Blueprint('games', __name__,
                        template_folder='templates/game', url_prefix="/game")


@game_gp.route("/<game_id>/<inject_id>")
def games_page(game_id, inject_id):
    template_name = "choice_inject.html"
    if int(inject_id) % 2 == 0:
        template_name = "informative_inject.html"
    return render_template(template_name, game_id=game_id)
