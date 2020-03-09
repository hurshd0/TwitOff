from flask import Blueprint, render_template

error_routes = Blueprint("error_routes", __name__)


@error_routes.app_errorhandler(404)
def error_404(error):
    return render_template("error.html"), 404
