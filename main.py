from flask import Flask, jsonify, render_template
import os
from db import init_db
from auth import login_required, register_auth_routes

# Initialize Flask app
app = Flask(__name__, template_folder="templates")

# Configuration
app.config["DEBUG"] = True
app.config["JSON_SORT_KEYS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "your-secret-key-here")

# Initialize database
init_db()

# Register authentication routes
register_auth_routes(app)


# Routes
@app.route("/")
@login_required
def home():
    return render_template("index.html")


@app.route("/api/hello", methods=["GET", "POST"])
@login_required
def api_hello():
    from flask import request
    if request.method == "POST":
        data = request.get_json()
        name = data.get("name", "World")
        return jsonify({"message": f"Hello, {name}!"})
    return jsonify({"message": "Hello, World!"})


@app.route("/api/data", methods=["GET"])
@login_required
def api_data():
    return jsonify({
        "status": "success",
        "data": [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"}
        ]
    })


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("FLASK_ENV") == "development",
    )


