"""Main application and routing logic for TwitOff."""
from decouple import config
from flask import Flask, render_template, request, url_for, redirect
from .models import db, User, Tweet
from .twitter import add_or_update_user, update_all_users, add_users, TWITTER_USERS
from .predict import predict_user


def create_app():
    """Create and configure and instance of flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/')
    def get_home():
        return render_template('index.html', title='Home')

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

    @app.route('/predictions')
    def get_predictions():
        users = User.query.all()
        if not users:
            add_users(TWITTER_USERS)
        return render_template("predictions.html", title='Predictions', users=users)

    @app.route('/user', methods=['POST'])
    def add_user(error_message=None, success_message=None):
        try:
            username = request.form.get('username')
            users = User.query.all()
            user_handle_list = [user.handle for user in users]
            if username in user_handle_list:
                success_message = f'User {username} already added, updating user tweets!'
                add_or_update_user(username)
                print(f'[DEBUG] {success_message}')
            else:
                add_or_update_user(username)
                success_message = "User {} successfully added!".format(
                    username)
                print(f'[DEBUG] {success_message}')
        except Exception as e:
            error_message = "Error adding {}: {}".format(username, e)
            print(f'[DEBUG] {error_message}')
            tweets = []
        return render_template("predictions.html", title='Predictions', users=users, success_message=success_message, error_message=error_message)

    @app.route('/user/<username>', methods=['GET'])
    def get_user_info(username=None):
        tweets = User.query.filter(User.handle == username).one().tweets
        return render_template('user.html', title=username, tweets=tweets)

    @app.route('/compare', methods=['POST'])
    def compare(compare_message=None, compare_error_message=None):
        users = User.query.all()
        user1, user2 = sorted([request.values['user1'],
                               request.values['user2']])
        if user1 == user2:
            compare_error_message = 'Cannot compare a user to themselves!'
        else:
            tweet_text = request.values['tweet_text']
            confidence = int(predict_user(user1, user2, tweet_text) * 100)
            if confidence >= 50:
                compare_message = f'"{tweet_text}" is more likely to be said by {user1} than {user2}, with {confidence}% confidence'
            else:
                compare_message = f'"{tweet_text}" is more likely to be said by {user2} than {user1}, with {100-confidence}% confidence'
        return render_template('predictions.html', title='Prediction', compare_message=compare_message, compare_error_message=compare_error_message, users=users)

    return app
