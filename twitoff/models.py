"""SQLAlchemy models for TwitOff."""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    """Twitter users that we pull and analyze Tweets for."""
    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(15), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.handle


class Tweet(db.Model):
    """Tweets."""
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Unicode(280))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tweets', lazy=True))

    def __repr__(self):
        return '<Tweet %r>' % self.text
