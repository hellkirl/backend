from flask import Blueprint, render_template
from flask_login import login_required

from migrations import db

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("start.html")

@login_required
@main.route("/dashboard")
def profile():
    return "Dashboard"
