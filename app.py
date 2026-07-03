import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from backend.model import get_response

# 1. Load environment variables
load_dotenv()

# 2. Setup Database Path
db_path = os.getenv("CHROMA_DB_PATH", "db")

# Automatically run ingestion if database doesn't exist
if not os.path.exists(db_path):
    print("Database not found. Initializing ingestion...")
    os.system("python backend/ingest_data.py")

# 3. Flask App Setup
app = Flask(__name__)
CORS(app)

# 4. Routes
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "LLMOps Personal Productivity Assistant"})

@app.route("/query", methods=["POST"])
def query_assistant():
    data = request.get_json()

    # Input validation
    if not data or "query" not in data:
        return jsonify({"error": "Invalid request. 'query' field is required."}), 400

    user_query = data.get("query", "").strip()

    if not user_query:
        return jsonify({"error": "Query cannot be empty."}), 400

    try:
        # Call RAG logic from backend/model.py
        response = get_response(user_query)
        return jsonify({"response": response})

    except Exception as e:
        # Detailed logging for debugging
        print(f"Backend Error: {e}")
        return jsonify({"error": str(e)}), 500

# 5. Run Server
if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 8080))
    print(f"Server starting on port {PORT}...")
    app.run(host="0.0.0.0", port=PORT, debug=True)