from flask import render_template, Blueprint
from twitoff.models import User

home_routes = Blueprint("home_routes", __name__)


@home_routes.route('/')
def get_home():
    users = User.query.all()
    return render_template('index.html', title='Home', users=users)
