from flask import render_template, Blueprint, request, jsonify
from twitoff.twitter import add_users, TWITTER_USERS
from twitoff.models import User
from twitoff.predict import predict_user


compare_routes = Blueprint("compare_routes", __name__)


@compare_routes.route('/predictions')
def get_predictions():
    users = User.query.all()
    if not users:
        add_users(TWITTER_USERS)
    return render_template("predictions.html", title='Predictions', users=users)


@compare_routes.route('/compare', methods=['POST'])
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


@compare_routes.route('/tcompare', methods=['POST'])
def temp_compare():

    data = request.get_json(force=True)
    print(data)

    users = [user.handle for user in User.query.all()]
    print(users)

    user1, user2 = sorted([data['user1'],
                           data['user2']])
    if user1 == user2:
        message = 'Cannot compare a user to themselves!'
        success = False
    elif (user1 not in users) or (user2 not in users):
        message = f'Neither of User 1: {user1} or User 2: {user2} found!'
        success = False
    else:
        tweet_text = data['tweet_text']
        confidence = int(predict_user(user1, user2, tweet_text) * 100)
        if confidence >= 50:
            message = f'"{tweet_text}" is more likely to be said by {user1} than {user2}, with {confidence}% confidence'
        else:
            message = f'"{tweet_text}" is more likely to be said by {user2} than {user1}, with {100-confidence}% confidence'
        success = True
    return jsonify({'success': success, 'message': message})


@compare_routes.route('/temp')
def temp():
    return render_template('temp.html', title='Temp')
