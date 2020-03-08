from flask import Blueprint, request, jsonify
from twitoff.twitter import add_or_update_user, update_all_users, add_users, TWITTER_USERS
from twitoff.models import db, User, Tweet

user_routes = Blueprint("user_routes", __name__)


@user_routes.route('/user', methods=['POST'])
def add_user(message=None):
    try:
        data = request.get_json(force=True)
        username = data['username']
        users = User.query.all()
        user_handle_list = [user.handle for user in users]
        if username in user_handle_list:
            message = f'User {username} already added, updating user tweets!'
            add_or_update_user(username)
            print(f'[DEBUG] {message}')
        else:
            add_or_update_user(username)
            message = "User {} successfully added!".format(
                username)
            print(f'[DEBUG] {message}')
        success = True
    except Exception as e:
        message = "Error adding {}: {}".format(username, e)
        print(f'[DEBUG] {message}')
        success = False
    return jsonify({'success': success, 'message': message})


@user_routes.route('/user/<username>', methods=['GET'])
def get_user_info(username=None):
    try:
        tweets = User.query.filter(User.handle == username).one().tweets
        success = True
        message = f"Successfully fetched Tweets for {username}"
    except Exception as e:
        tweets = []
        success = False
        message = "Error getting tweets for {}: {}".format(username, e)
        print(f'[DEBUG] {message}')
    return jsonify({"success": success, "message": message, "data": tweets})


@user_routes.route('/update')
def update():
    users = User.query.all()
    update_all_users()
    return jsonify({"success":True, "message": "Upated all user tweets."})


@user_routes.route('/delete/<username>', methods=['DELETE'])
def delete_user(username):
    try:
        user = User.query.filter(User.handle == username).one()
        db.session.delete(user)
        db.session.commit()
        success = True
        message = f'{user } has been sucessfully deleted.'
        print(f"[DEBUG] {message}")
    except Exception as e:
        success = False
        message = "User not found."
    return jsonify({'success': success, 'message': message})
