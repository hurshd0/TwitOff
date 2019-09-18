"""Main application and routing logic for TwitOff."""
from decouple import config
from flask import Flask, render_template, request, url_for, redirect
from .models import db, User, Tweet
from .twitter import add_or_update_user, update_all_users, add_users, TWITTER_USERS


def create_app():
    """Create and configure and instance of flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ENV'] = config('FLASK_ENV')
    db.init_app(app)

    @app.route('/')
    def index():
        users = User.query.all()
        if not users:
            add_users(TWITTER_USERS)
        return render_template('index.html', title='Home', users=users)

    @app.route('/reset')
    def reset():
        db.drop_all()
        db.create_all()
        return render_template('index.html', title='Reset - Database!', users=[])

    @app.route('/update')
    def update():
        update_all_users()
        users = User.query.all()
        return render_template('index.html', title='Update all users!', users=users)

    @app.route('/about')
    def about():
        return render_template("about.html", title='About TwitOff')

    @app.route('/user', methods=['POST'])
    @app.route('/user/<username>', methods=['GET'])
    def user(username=None, message=''):
        username = username or request.values['username']
        try:
            if request.method == 'POST':
                add_or_update_user(username)
                message = "User {} successfully added!".format(username)
            tweets = User.query.filter(User.handle == username).one().tweets
        except Exception as e:
            message = "Error adding {}: {}".format(username, e)
            tweets = []
        return render_template('user.html', title=username, tweets=tweets, message=message)

    return app
