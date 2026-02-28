import os

is_production = os.environ.get("FLASK_ENV") == "production"

# Auth
REQUIRE_LOGIN = is_production or True  # flip to False to disable in dev

# Flask config
DEBUG = not is_production
JSON_SORT_KEYS = False
PORT = int(os.environ.get("PORT", 5000))

# Secret key
if is_production:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set in production")
else:
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(24))