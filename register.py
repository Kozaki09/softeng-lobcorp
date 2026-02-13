from flask import Blueprint, render_template, request, redirect, url_for
from database import get_db

register_bp = Blueprint("register", _name_)

@register_bp.route("/register", methods=["GET", "POST"])

def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        if not name or not email or not password: 
            return "All fields required"
    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    ).fetchone()

    if user: 
        conn.close()
        return "email already exists"
    conn.execute(
        "INSER INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password)
    )
    conn.commit()
    conn.close()

    return redirect(url_for(login.login))

    return render_template("register.html")