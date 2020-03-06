"""Main application and routing logic for TwitOff."""
from decouple import config
from flask import Flask, Blueprint, jsonify, render_template, request, url_for, redirect
from twitoff.models import db
from twitoff.routes.compare_routes import compare
from twitoff.routes.home_routes import home
from twitoff.routes.user_routes import user


def create_app():
    """Create and configure and instance of flask application."""
    app = Flask(__name__)

    # Set DB config
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize db
    db.init_app(app)

    # Register routes
    app.register_blueprint(home)
    app.register_blueprint(user)
    app.register_blueprint(compare)

    return app
