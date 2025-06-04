import os
from flask import Flask, request, jsonify
from google.oauth2 import service_account
from google.cloud import firestore
from agents.gemini_agent import GeminiAgent

# Load Service Account
creds = service_account.Credentials.from_service_account_file("secrets/service-account.json")

# Firestore
db = firestore.Client(credentials=creds)

# Gemini
PROJECT_ID = "agent-factory-adk"
LOCATION = "us-central1"
agent = GeminiAgent(project_id=PROJECT_ID, location=LOCATION)

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask_agent():
    print("Received /ask POST request")  # Add this line
    data = request.get_json()
    prompt = data.get("prompt", "")
    print(f"Prompt: {prompt}")  # Add this line
    response = agent.run(prompt)

    db.collection("agent_logs").add({"prompt": prompt, "response": response})
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


@app.route("/", methods=["GET"])
def index():
    return "✅ Agent Factory ADK is running. POST to /ask with a JSON prompt."
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404