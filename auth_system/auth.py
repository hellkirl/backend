from flask import Blueprint, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from migrations.db import Connector
from config import DATABASE, USERNAME, PASSWORD, PORT
from models import User

auth = Blueprint("auth", __name__)

c = Connector(database=DATABASE, username=USERNAME, password=PASSWORD)
con, cur = c.connect()


@auth.route("/login")
def login():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]

        cur.execute("SELECT password FROM users WHERE login = %s", (login,))
        acquired_password = cur.fetchone()

        if bcrypt.checkpw(password, acquired_password):
            return app.redirect("/dashboard")
        else:
            return app.redirect("/login")

    return render_template("login.html")

    return render_template("login.html")


@auth.route('/signup')
def signup():
    return render_template("register.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        login = request.form["login"]
        password = request.form["password"]

        user = User(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, login=login,
                    password=password)

        if user.check():
            print(f"The email is already in use")
        else:
            user.create()

        return app.redirect("/dashboard")

    return render_template("register.html")


@auth.route("/logout")
def logout():
    return "Logout"
