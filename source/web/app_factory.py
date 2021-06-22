import yaml

from flask import Flask

from globalconfig import config
from web.game_blueprint import game_gp
from web.index_blueprint import index_gp


class AppFactory:
    @staticmethod
    def create_app():
        """ Flask application factory """

        # Setup Flask and load app.config
        new_app = Flask(__name__)
        # new_app.config.from_file("web_config.yml", load=yaml.safe_load)
        new_app.config.update(config.get_flask_config)

        new_app.register_blueprint(index_gp)
        new_app.register_blueprint(game_gp)

        return new_app
