from flask import render_template, Blueprint, request
from twitoff.twitter import add_or_update_user, update_all_users, add_users, TWITTER_USERS
from twitoff.models import db, User, Tweet

user = Blueprint("user", __name__)


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


@app.route('/update')
def update():
    update_all_users()
    users = User.query.all()
    return render_template('index.html', title='Update all users!', users=users)


@home.route('/reset')
def reset():
    db.drop_all()
    db.create_all()
    return render_template('index.html', title='Reset - Database!', users=[])
