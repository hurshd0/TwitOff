import tweepy
from decouple import config
from .models import db, Tweet, User

TWITTER_AUTH = tweepy.OAuthHandler(
    config('TWITTER_CONSUMER_KEY'), config('TWITTER_CONSUMER_SECRET_KEY'))
TWITTER_AUTH.set_access_token(
    config('TWITTER_ACCESS_TOKEN'), config('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)
