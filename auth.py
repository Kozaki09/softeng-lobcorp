"""Authentication routes and utilities"""
from flask import render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from db import get_user_by_username, create_user


def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


def register_auth_routes(app):
    """Register authentication routes to the Flask app"""

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            if not username or not password:
                flash("Username and password are required", "error")
                return render_template("login.html")

            user = get_user_by_username(username)

            if user and check_password_hash(user["password_hash"], password):
                session["user_id"] = user["username"]
                session["user_email"] = user["email"]
                return redirect(url_for("home"))
            else:
                flash("Invalid username or password", "error")

        return render_template("login.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            email = request.form.get("email")

            if not username or not password:
                flash("Username and password are required", "error")
                return render_template("register.html")

            password_hash = generate_password_hash(password)
            success = create_user(username, password_hash, email)

            if success:
                flash("Account created successfully! Please log in.", "success")
                return redirect(url_for("login"))
            else:
                flash("Username already exists", "error")

            return render_template("register.html")

        return render_template("register.html")

    @app.route("/logout")
    def logout():
        session.pop("user_id", None)
        session.pop("user_email", None)
        return redirect(url_for("login"))
