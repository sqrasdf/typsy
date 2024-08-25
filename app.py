from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

import sqlite3
from random import randint
import re
import datetime

app = Flask(__name__)

app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def index():
    user_id = session.get("user_id")
    print("\n\nuser_id:", user_id, "\n\n")
    return render_template("index.html", user_id=user_id)


@app.route("/get_data")
def get_data():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    words = []
    counter = int(cur.execute("SELECT COUNT(*) FROM words;").fetchone()[0]) - 1
    for i in range(15):
        res = cur.execute(
            "SELECT word FROM words WHERE id = ?;",
            (randint(0, counter),
        )).fetchone()[0]
        words.append(res)
    return {"words": " ".join(words)}


@app.route("/get_games_data", methods=["POST"])
def get_games_data():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        if not user_id:
            return render_template("error.html", message="no user_id")
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        try:
            res = cur.execute("SELECT date, wpm, accuracy FROM user_data WHERE user_id = ?;", (7, )).fetchall()
        except Exception as error:
            return render_template("error.html", message=error)
        return str(res)
    return "/get_games_data\nit should not be visible i guess"
    

@app.route("/send_data", methods=["GET", "POST"])
def send_data():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    if request.method == "POST":
        user_id = session["user_id"]
        wpm = request.form.get("wpm")
        accuracy = request.form.get("accuracy")
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cur.execute("INSERT INTO user_data VALUES (NULL, ?, ?, ?, ?);", (user_id, wpm, accuracy, date))
        con.commit()

    res = cur.execute("SELECT * FROM user_data;").fetchall()
    return "<br>".join(" ".join([str(i) for i in item]) for item in res)
    

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if not username:
            return render_template("error.html", message="no username")
        if not email:
            return render_template("error.html", message="no email")
        if not password:
            return render_template("error.html", message="no password")
        if not bool(re.match(r"^\S+@\S+\.\S+$", email)):
            return render_template("error.html", message="email is not valid")

        try:
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute("INSERT INTO users VALUES (NULL, ?, ?, ?, ?);", (username, email, password, generate_password_hash(password)))
            con.commit()
        except:
            return render_template("error.html", message="username is already in use")

        try:
            user_id = cur.execute("SELECT id FROM users WHERE username = ?;", (username, )).fetchone()[0]
            session["user_id"] = user_id
        except Exception as error:
            return render_template("error.html", message=error)

        return redirect("/")

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        print("username", username)
        email = request.form.get("email")
        password = request.form.get("password")
        if not username:
            return render_template("error.html", message="no username")
        if not email:
            return render_template("error.html", message="no email")
        if not password:
            return render_template("error.html", message="no password")
        if not bool(re.match(r"^\S+@\S+\.\S+$", email)):
            return render_template("error.html", message="email is not valid")

        try:
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            res = cur.execute("SELECT id, password_hash FROM users WHERE username = ?;", (username, )).fetchone()
            user_id = res[0]
            p_hash = res[1]
            print(user_id, p_hash)
            if check_password_hash(p_hash, password):
                session["user_id"] = user_id
                return redirect("/")
            return render_template("error.html", message="password is not correct")
            
        except Exception as error:
            return render_template("error.html", message=error)


        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/profile")
@login_required
def profile():
    user_id = session["user_id"]
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    username = cur.execute("SELECT username FROM users WHERE id = ?;", (user_id, )).fetchone()[0]
    max_wpm, avg_accuracy = cur.execute("SELECT MAX(wpm), AVG(accuracy) FROM user_data WHERE user_id = ?;", (7, )).fetchall()[0]
    return render_template("profile.html", username=username, max_wpm=round(max_wpm, 2), avg_accuracy=round(avg_accuracy, 2))




# if __name__ == "__main__":
#     app.run(debug=True)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0")