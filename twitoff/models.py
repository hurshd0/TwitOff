"""SQLAlchemy models for TwitOff."""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    """Twitter users that we pull and analyze Tweets for."""
    id = db.Column(db.BigInteger, primary_key=True)
    handle = db.Column(db.String(15), unique=True, nullable=False)
    profile_image_url = db.Column(db.Text)
    followers_count = db.Column(db.BigInteger)
    following_count = db.Column(db.BigInteger)
    newest_tweet_id = db.Column(db.BigInteger)

    def __repr__(self):
        return '<User %r>' % self.handle


class Tweet(db.Model):
    """Tweets."""
    id = db.Column(db.BigInteger, primary_key=True)
    text = db.Column(db.Unicode(300), nullable=False)
    embedding = db.Column(db.PickleType, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey(
        'user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tweets', lazy=True))

    def __repr__(self):
        return '<Tweet %r>' % self.text
