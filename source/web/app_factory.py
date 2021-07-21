from flask import Flask

from globalconfig import config
from web.api_blueprint import api_bp
from web.game_blueprint import game_gp
from web.index_blueprint import index_gp
from web.scenario_blueprint import scenario_bp


class AppFactory:
    @staticmethod
    def create_app():
        """ Flask application factory """

        # Setup Flask and load app.config
        new_app = Flask(__name__)
        new_app.config.update(config.get_flask_config())

        new_app.register_blueprint(index_gp)
        new_app.register_blueprint(game_gp)
        new_app.register_blueprint(scenario_bp)
        new_app.register_blueprint(api_bp)

        new_app.url_map.strict_slashes = False


        return new_app
