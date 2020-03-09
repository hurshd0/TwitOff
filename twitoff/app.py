"""Main application and routing logic for TwitOff."""
from decouple import config
from flask import Flask
from twitoff.routes.compare_routes import compare_routes
from twitoff.routes.home_routes import home_routes
from twitoff.routes.user_routes import user_routes
from twitoff.routes.error_routes import error_routes


def create_app():
    """Application Factory Pattern"""
    """Create and configure and instance of flask application."""
    app = Flask(__name__)

    # Configures DB
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize, and migrating DB
    from twitoff.models import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Registering routes
    app.register_blueprint(home_routes)
    app.register_blueprint(user_routes)
    app.register_blueprint(compare_routes)
    app.register_blueprint(error_routes)

    return app
