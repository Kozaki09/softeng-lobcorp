from flask import Flask, jsonify, render_template, request
import os
from db import init_db
from auth import login_required, register_auth_routes
#from models.predict import predict_basic, predict_basic_exapanded, predict_advanced

# Initialize Flask app
app = Flask(__name__, template_folder="templates")

# Configuration
app.config["DEBUG"] = True
app.config["JSON_SORT_KEYS"] = False

if os.environ.get("FLASK_ENV") == "production":
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    if not app.config["SECRET_KEY"]:
        raise ValueError("SECRET_KEY environment variable must be set in production")
else:
    # Dev/debug: random key resets all sessions on restart
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", os.urandom(24))

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
    return render_template("subscription.html")

@app.route("/predict", methods=["POST"])
def predict():
    mode = request.form.get("mode") or "basic"

    form = {
        "age": request.form.get("age") or None,
        "sex": request.form.get("sex") or None,
        "cp": request.form.get("cp") or None,
        "trestbps": request.form.get("trestbps") or None,
        "chol": request.form.get("chol") or None,
        "fbs": request.form.get("fbs") or None,
        "restecg": request.form.get("restecg") or None,
        "thalach": request.form.get("thalach") or None,
        "exang": request.form.get("exang") or None,
        "oldpeak": request.form.get("oldpeak") or None,
        "slope": request.form.get("slope") or None,
        "ca": request.form.get("ca") or None,
        "thal": request.form.get("thal") or None,
    }

    if mode == "basic":
        if form.chol is not None or form.fbs is not None:
            # call expanded model function
            pass
        else:
            # call basic model function
            pass
    elif mode == "advanced":
        # call advanced model function
        pass
    else:
        return jsonify({"error": "Invalid mode"}), 400


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


