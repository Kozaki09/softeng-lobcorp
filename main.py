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
    user_id = session.get("user_id")
    sub     = get_active_subscription(user_id)
    plan    = "premium" if sub else "free"
    return render_template("index.html", plan=plan)

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
        activate_subscription(user_id)

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
@login_required
def predict():
    mode = request.form.get("mode", "basic")

    if mode not in ["bare", "basic", "advanced"]:
        return jsonify({"error": "Invalid mode"}), 400
    
    if not request.form:
        return jsonify({"error": "No input provided"}), 400

    form = {
        "age": request.form.get("age"),
        "sex": request.form.get("sex"),
        "cp": request.form.get("cp"),
        "trestbps": request.form.get("trestbps"),
        "chol": request.form.get("chol"),
        "fbs": request.form.get("fbs"),
        "restecg": request.form.get("restecg"),
        "thalach": request.form.get("thalach"),
        "exang": request.form.get("exang"),
        "oldpeak": request.form.get("oldpeak"),
        "slope": request.form.get("slope"),
        "ca": request.form.get("ca"),
        "thal": request.form.get("thal"),
    }
    
    results = predict_risk(form, mode)
    if "error" in results:
        return jsonify(results), 400
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
        debug=DEBUG,
    )