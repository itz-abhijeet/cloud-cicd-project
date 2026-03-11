import os
from flask import Flask, render_template, jsonify
from datetime import datetime

application = Flask(__name__)

# --- Application Metadata ---
APP_NAME = "CIDI DevOps Pipeline"
APP_VERSION = "1.0.0"
ENVIRONMENT = os.environ.get("APP_ENV", "production")


@application.route("/")
def home():
    """Home route — renders the main landing page."""
    context = {
        "app_name": APP_NAME,
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "year": datetime.utcnow().year,
    }
    return render_template("index.html", **context)


@application.route("/status")
def status():
    """Health-check / status route — returns JSON for monitoring tools."""
    payload = {
        "status": "healthy",
        "app": APP_NAME,
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "uptime": "OK",
    }
    return jsonify(payload), 200


@application.route("/health")
def health():
    """Lightweight liveness probe used by Elastic Beanstalk / ALB health checks."""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    application.run(host="0.0.0.0", port=port, debug=(ENVIRONMENT != "production"))
