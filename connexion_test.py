import os
import time
from flask import Flask, jsonify
from flask_pymongo import PyMongo
from pymongo.errors import ConnectionFailure, ConfigurationError

# Load environment variables if present
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

# ✅ MongoDB URI must include the database name
app.config["MONGO_URI"] = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://<username>:<password>@cluster0.mongodb.net/task_manager?retryWrites=true&w=majority"
)
app.secret_key = os.environ.get("SECRET_KEY", "supersecret")

# Initialize PyMongo
mongo = PyMongo(app)


def check_mongo_connection(max_retries=3, delay=3):
    """
    Attempts to connect to MongoDB Atlas.
    Retries `max_retries` times with `delay` seconds between attempts.
    """
    for attempt in range(1, max_retries + 1):
        try:
            print(f"🔄 Attempt {attempt}/{max_retries} — Pinging MongoDB Atlas...")
            mongo.cx.admin.command("ping")  # Test the connection
            db_name = mongo.db.name if mongo.db else "Unknown Database"
            print(f"✅ Successfully connected to MongoDB Atlas — Database: {db_name}")
            return True, db_name
        except (ConnectionFailure, ConfigurationError) as e:
            print(f"⚠️  Connection failed (attempt {attempt}): {e}")
            if attempt < max_retries:
                print(f"⏳ Retrying in {delay} seconds...\n")
                time.sleep(delay)
            else:
                print("❌ All connection attempts failed.")
                return False, None


@app.route("/check_db")
def check_db_connection():
    """Endpoint to verify MongoDB Atlas connectivity with retry logic."""
    success, db_name = check_mongo_connection()
    if success:
        return jsonify({
            "status": "success",
            "message": f"Connected to MongoDB Atlas — Database: {db_name}"
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Failed to connect to MongoDB Atlas after multiple attempts. Please check your URI or network connection."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
