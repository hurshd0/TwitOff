"""Main application and routing logic for TwitOff."""
from decouple import config
from flask import Flask, render_template, request
from .models import db, User


def create_app():
    """Create and configure and instance of flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['ENV'] = config('ENV')
    db.init_app(app)

    @app.route('/')
    def index():
        users = User.query.all()
        return render_template('index.html', title='Home', users=users)

    return app
