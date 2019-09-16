"""Main application and routing logic for TwitOff."""

from flask import Flask
from .models import db


def create_app():
    """Create and configure and instance of flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    db.init_app(app)

    @app.route('/')
    def index():
        return 'Welcome to TwitOff!'

    return app
