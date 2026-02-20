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
@app.route("/index")
@app.route("/home")
@login_required
def index():
    return render_template("index.html")

@app.route('/components/<name>')
def component(name):
    return render_template(f'components/{name}.html')

@app.route("/subscribe")
def subscribe():
    return render_template("register.html")

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


