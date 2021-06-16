import json

from flask import Flask, render_template_string
from flask_mongoengine import MongoEngine
from flask_user import login_required, UserManager, UserMixin

from game_blueprint import game_gp
from web.index_blueprint import index_gp


class AppFactory:
    @staticmethod
    def create_app():
        """ Flask application factory """

        # Setup Flask and load app.config
        new_app = Flask(__name__)
        new_app.config.from_file("config.json", load=json.load)

        # Setup Flask-MongoEngine
        db = MongoEngine(new_app)

        # Define the User document.
        # NB: Make sure to add flask_user UserMixin !!!
        class User(db.Document, UserMixin):
            active = db.BooleanField(default=True)

            # User authentication information
            username = db.StringField(default='')
            password = db.StringField()

            # User information
            first_name = db.StringField(default='')
            last_name = db.StringField(default='')
            organization = db.StringField(default='')

            # Relationships
            roles = db.ListField(db.StringField(), default=[])

        # Setup Flask-User and specify the User data-model
        user_manager = UserManager(new_app, db, User)

        new_app.register_blueprint(index_gp)
        new_app.register_blueprint(game_gp)

        return new_app
