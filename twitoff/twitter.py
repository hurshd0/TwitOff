import tweepy
import basilica
from decouple import config
from .models import db, Tweet, User

# https://greatlist.com/happiness/must-follow-twitter-accounts
TWITTER_USERS = ['calebhicks', 'elonmusk', 'rrherr', 'SteveMartinToGO',
                 'alyankovic', 'nasa', 'sadserver', 'jkhowland', 'austen',
                 'common_squirrel', 'KenJennings', 'connanobrien',
                 'big_ben_clock', 'IAM_SHAKESPEARE']

TWITTER_AUTH = tweepy.OAuthHandler(
    config('TWITTER_CONSUMER_KEY'), config('TWITTER_CONSUMER_SECRET_KEY'))
TWITTER_AUTH.set_access_token(
    config('TWITTER_ACCESS_TOKEN'), config('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(config('BASILICA_KEY'))


def add_or_update_user(username):
    """Add or update a user and their tweets, else error if not a Twitter user."""
    try:
        twitter_user = TWITTER.get_user(username)  # Fetch twitter user handle
        # Create SQLAlchemy User db instance
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id, handle=username, followers_count=twitter_user.followers_count, following_count=twitter_user.friends_count))

        # Add user to database
        db.session.add(db_user)

        # Fetch tweets as many as recent as possible with no RT's/Replies.
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False, tweet_mode='extended', since_id=db_user.newest_tweet_id)

        # Check if new or recent tweets exists, if does, get their recent most
        # tweet id
        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # Loop through newly fetched tweets
        for tweet in tweets:
            # Calculate embedding on the full tweet, but truncate for storing
            embedding = BASILICA.embed_sentence(
                tweet.full_text, model='twitter')
            db_tweet = Tweet(
                id=tweet.id, text=tweet.full_text[:300], embedding=embedding)
            db_user.tweets.append(db_tweet)
            # Add tweets to the database
            db.session.add(db_tweet)

    except Exception as e:
        print(e)
    finally:
        db.session.commit()


def update_all_users():
    """Update all Tweets for all Users in the User table."""
    for user in User.query.all():
        add_or_update_user(user.name)


def add_users(users):
    """Add/Update a list of users for debugging database."""
    for user in users:
        add_or_update_user(user)


def debug_twitter_json(username):
    """Use it debug user's data"""
    user_info = {}
    twitter_user = TWITTER.get_user(username)
    user_info['user_name'] = twitter_user.screen_name
    user_info['user_id'] = twitter_user.id
    user_info['profile_image'] = twitter_user.profile_image_url_https
    user_info['follower_count'] = twitter_user.followers_count
    user_info['following_count'] = twitter_user.friends_count
    user_info['raw_tweets'] = twitter_user.timeline(
        count=200, exclude_replies=True, include_rts=False, tweet_mode='extended')
    return user_info
