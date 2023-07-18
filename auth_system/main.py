from functools import wraps

import bcrypt
from flask import Flask, render_template, request, session, url_for
from flask_migrate import Migrate

from config import DATABASE, PASSWORD, USERNAME
from database.db import Connector

app = Flask(__name__)

c = Connector(database=DATABASE, username=USERNAME, password=PASSWORD)
con, cur = c.connect()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return app.redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/logout")
@login_required
def logout():
    session.pop("logged_in", None)
    return app.redirect("/")


@app.route("/")
def index():
    return render_template("start.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        login = request.form["login"]
        salt = str(bcrypt.gensalt())
        pw_hash = bcrypt.hashpw(request.form["password"].encode("utf-8"), bytes(salt))

        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            print("The registration is not possible. The email is already in use!")
        else:
            cur.execute("""INSERT INTO users (first_name, last_name, email, phone_number, login, password)
                        VALUES (%s, %s, %s, %s, %s, %s)""",
                        (first_name, last_name, email, phone_number, login, password))
            return app.redirect("/dashboard")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form["login"]
        password = bcrypt.hashpw(request.form["password"].encode("utf-8"), bcrypt.gensalt())

        cur.execute("SELECT password FROM users WHERE login = %s", (login,))
        acquired_password = cur.fetchone()

        if bcrypt.checkpw(password, acquired_password):
            return app.redirect("/dashboard")
        else:
            return app.redirect("/login")

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return "<b>You're logged in</b>"


if __name__ == "__main__":
    app.run()
