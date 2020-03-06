from flask import render_template, Blueprint


home_routes = Blueprint("home_routes", __name__)


@home_routes.route('/')
def get_home():
    return render_template('index.html', title='Home')
