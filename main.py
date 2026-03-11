from flask import Flask, jsonify, render_template, request, session
import os
from db import init_db, get_active_subscription, activate_subscription
from auth import login_required, register_auth_routes
from models.predict import predict_risk
from api.payment import register_payment_routes, get_price
from app_config import SECRET_KEY, DEBUG, JSON_SORT_KEYS

# Initialize Flask app
app = Flask(__name__, template_folder="templates")

# Configuration
app.config["SECRET_KEY"] = SECRET_KEY
app.config["DEBUG"] = DEBUG
app.config["JSON_SORT_KEYS"] = JSON_SORT_KEYS

# Initialize database
init_db()

# Register routes
register_auth_routes(app)
register_payment_routes(app)

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
@login_required
def subscribe():
    user_id = session["user_id"]
    username = session["username"]

    # PayMongo redirects here after successful payment
    # Activate immediately since webhook can't reach localhost
    if request.args.get("status") == "success":
        print(f"[DEBUG] activating subscription for user_id={user_id}")
        result = activate_subscription(user_id)
        print(f"[DEBUG] activate_subscription returned={result}")

    subscription = get_active_subscription(user_id)

    plan = "premium" if subscription else "free"

    return render_template(
        "subscription.html",
        plan = plan,
        subscription = subscription,
        username = username,
        price = get_price()
    )

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
    
    results = predict_risk(form, mode)
    # more to do here - log prediction, etc
    
    return jsonify(results)
    



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