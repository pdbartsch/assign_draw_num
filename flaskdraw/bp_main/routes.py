from flask import Blueprint

from flask import render_template, url_for, flash, redirect, request, abort
from flask import current_app

from flaskdraw.models import Drawfile
from flask_login import login_user, login_required

bp_main = Blueprint("bp_main", __name__)

@bp_main.route("/")
def index():
    return render_template(
        "index.html",
        title="Home Page",
        sidebar="homepage"
    )