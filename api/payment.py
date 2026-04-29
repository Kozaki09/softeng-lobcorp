import hashlib
import hmac
import os
import base64
import requests
from flask import jsonify, request, session, url_for
from auth import login_required
from db import get_active_subscription, activate_subscription, cancel_subscription

PAYMONGO_SECRET_KEY     = os.environ.get("PAYMONGO_SECRET_KEY", "")
PAYMONGO_WEBHOOK_SECRET = ""
PAYMONGO_BASE_URL       = "https://api.paymongo.com/v1"
PREMIUM_PRICE           = 99    # ₱99.00 — for display
PREMIUM_PRICE_CENTS     = 9900  # centavos — sent to PayMongo

def get_price():
    return PREMIUM_PRICE

def _auth_header():
    token = base64.b64encode(f"{PAYMONGO_SECRET_KEY}:".encode()).decode()
    return {"Authorization": f"Basic {token}", "Content-Type": "application/json"}

def _current_user():
    return session.get("user_id"), session.get("username")


def register_payment_routes(app):

    @app.route("/api/subscription/status", methods=["GET"])
    @login_required
    def subscription_status():
        user_id, _ = _current_user()
        sub = get_active_subscription(user_id)
        if sub:
            return jsonify({
                "plan":       "premium",
                "start_date": sub["start_date"],
                "end_date":   sub["end_date"],
                "status":     sub["status"],
            })
        return jsonify({"plan": "free", "subscription": None})

    @app.route("/api/subscription/checkout", methods=["POST"])
    @login_required
    def create_checkout():
        user_id, username = _current_user()

        # Build absolute URLs dynamically using the current request's host
        success_url = url_for('subscribe', _external=True) + "?status=success"
        cancel_url  = url_for('subscribe', _external=True) + "?status=cancelled"

        payload = {
            "data": {
                "attributes": {
                    "billing":            {"name": username},
                    "send_email_receipt": False,
                    "show_description":   True,
                    "show_line_items":    True,
                    "line_items": [{
                        "currency": "PHP",
                        "amount":   PREMIUM_PRICE_CENTS,
                        "name":     "Diagknows Premium",
                        "quantity": 1,
                    }],
                    "payment_method_types": ["card"],
                    "success_url": success_url,
                    "cancel_url":  cancel_url,
                    "metadata":    {"user_id": str(user_id), "username": username},
                }
            }
        }

        res = requests.post(
            f"{PAYMONGO_BASE_URL}/checkout_sessions",
            json=payload,
            headers=_auth_header(),
        )

        if res.status_code != 200:
            error_body = res.json()
            print(f"[PayMongo] checkout error={error_body}")
            return jsonify({"error": "Could not create checkout session", "details": error_body}), 502

        checkout_url = res.json()["data"]["attributes"]["checkout_url"]
        return jsonify({"checkout_url": checkout_url})

    @app.route("/api/subscription/cancel", methods=["POST"])
    @login_required
    def cancel_sub():
        user_id, _ = _current_user()
        found      = cancel_subscription(user_id)
        if not found:
            return jsonify({"error": "No active subscription found"}), 404
        return jsonify({"message": "Subscription cancelled.", "plan": "free"})

    @app.route("/api/webhook/paymongo", methods=["POST"])
    def paymongo_webhook():
        """
        Receives PayMongo events.
        Register in: PayMongo Dashboard → Developers → Webhooks
        Event: checkout_session.payment.paid
        For local dev, expose with: ngrok http 5000
        """
        raw_body   = request.get_data()
        sig_header = request.headers.get("Paymongo-Signature", "")

        if not _verify_signature(sig_header, raw_body):
            return jsonify({"error": "Invalid signature"}), 401

        event      = request.get_json()
        event_type = event["data"]["attributes"].get("type")
        attributes = event["data"]["attributes"].get("data", {}).get("attributes", {})

        if event_type == "checkout_session.payment.paid":
            user_id = attributes.get("metadata", {}).get("user_id")
            if user_id:
                activate_subscription(int(user_id))

        return jsonify({"received": True})


def _verify_signature(sig_header: str, raw_body: bytes) -> bool:
    if not PAYMONGO_WEBHOOK_SECRET:
        return True  # skip in dev until webhook secret is configured
    try:
        parts     = dict(p.split("=", 1) for p in sig_header.split(",") if "=" in p)
        timestamp = parts.get("t", "")
        signature = parts.get("te", "") or parts.get("li", "")
        signed    = f"{timestamp}.{raw_body.decode()}"
        expected  = hmac.new(
            PAYMONGO_WEBHOOK_SECRET.encode(),
            signed.encode(),
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(expected, signature)
    except Exception:
        return False