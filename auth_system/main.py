from functools import wraps

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from config import DATABASE, PASSWORD, PORT, SECRET_KEY, USERNAME
from migrations.db import Connector
from models import User

app = Flask(__name__)
app.secret_key = SECRET_KEY

c = Connector(DATABASE, USERNAME, PASSWORD, PORT)
con, cur = c.connect()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def index():
    if "logged_in" in session and session["logged_in"]:
        return redirect(url_for("dashboard"))
    else:
        return render_template("start.html")


@app.route("/dashboard")
@login_required
def dashboard():
    if "logged_in" in session and session["logged_in"]:
        return render_template("dashboard.html")
    else:
        return redirect(url_for("login"))


@app.route("/signup")
def signup():
    if "logged_in" in session and session["logged_in"]:
        return render_template("dashboard.html")
    else:
        return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    session.pop("logged_in", None)
    return redirect("/")


@app.route("/signup", methods=["POST"])
def signup_post():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]
        email = request.form["email"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        phone_number = request.form["phone_number"]

        user = User(
            login=login,
            password=generate_password_hash(password),
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )

        if user.check():
            user.create()
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            return redirect(url_for("login"))


@app.route("/login")
def login():
    if "logged_in" in session and session["logged_in"]:
        return redirect(url_for("dashboard"))
    else:
        return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]

        cur.execute("SELECT password FROM users WHERE login = %s", (login,))
        hashed_password = cur.fetchone()

        if hashed_password and check_password_hash(hashed_password[0], password):
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            return render_template("login_incorrect.html")


if __name__ == "__main__":
    app.run(debug=True)
