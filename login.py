from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey"

def get_db_connection():
    conn = sqlite3.connect("user.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    if username == "" or password == "":
        return render_template("login.html", 
                               error="please fill all fields")
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        session["user"] = username
        return redirect(url_for(dashboard))
    else:
        return render_template("login.html", 
                               error="Invalid credentials")
    
@app.route("/dashboard")
def dashboard():
    if "user" in session: 
        return render_template("dashboard.html",
                               username=session["user"])
    return redirect(url_for("login_page"))

app.run(debug=True)