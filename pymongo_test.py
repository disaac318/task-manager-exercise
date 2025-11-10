import os
from flask import Flask, jsonify
from flask_pymongo import PyMongo
from pymongo.errors import ConnectionFailure

# Load env variables if available (useful for local development)
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

# ✅ MongoDB connection string (must include DB name!)
app.config["MONGO_URI"] = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://shuttermaven_db_user:CEorNGltYuxH6TF9@myclusterdb01.crvzcna.mongodb.net/?appName=MyClusterDB01"
)
app.secret_key = os.environ.get("SECRET_KEY", "supersecret")

mongo = PyMongo(app)

@app.route("/check_db")
def check_db_connection():
    """Check if Flask-PyMongo can connect to MongoDB Atlas."""
    try:
        # Ping MongoDB server
        mongo.cx.admin.command("ping")

        # Get database name for confirmation
        db_name = mongo.db.name if mongo.db else "No database selected"

        print(f"✅ Successfully connected to MongoDB Atlas — Database: {db_name}")
        return jsonify({
            "status": "success",
            "message": f"Connected to MongoDB Atlas — Database: {db_name}"
        }), 200

    except ConnectionFailure as e:
        print(f"❌ MongoDB connection failed: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to connect to MongoDB Atlas. Please check your URI or network connection."
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
