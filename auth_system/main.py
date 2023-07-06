from flask import Flask, request, render_template
import bcrypt
from flask_migrate import Migrate

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

from database.db import Connector
from config import DATABASE, USERNAME, PASSWORD

app = Flask(__name__)

c = Connector(database=DATABASE, username=USERNAME, password=PASSWORD)
con, cur = c.connect()


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
        password = bcrypt.hashpw(request.form["password"].encode("utf-8"), bcrypt.gensalt())

        cur.execute("SELECT * FROM users WHERE login = %s", (login,))
        if cur.fetchone():
            print("The registration is not possible. The user already exists!")
        else:
            cur.execute("""INSERT INTO users (first_name, last_name, email, phone_number, login, password)
                        VALUES (%s, %s, %s, %s, %s, %s)""",
                        (first_name, last_name, email, phone_number, login, password))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form["login"]
        password = bcrypt.hashpw(request.form["password"].encode("utf-8"), bcrypt.gensalt())

        cur.execute("SELECT password FROM users WHERE login = %s", (login,))
        acquired_password = cur.fetchone()

        if password == acquired_password:
            app.redirect("")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return "<b>You're loggin in</b>"


if __name__ == "__main__":
    app.run()
