# ============================================================
# AI Universe - Flask Backend Server
# ============================================================
# Installation Commands:
# pip install flask flask-cors groq
# ============================================================

# ------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os

# ------------------------------------------------------------
# FLASK SETUP
# ------------------------------------------------------------
app = Flask(__name__)

# Enable CORS for all routes and origins
# This allows your frontend (VS Code Live Server) to communicate with this backend
CORS(app)

# ------------------------------------------------------------
# GROQ CLIENT SETUP
# ------------------------------------------------------------
# Replace 'YOUR_GROQ_API_KEY' with your actual Groq API key
# You can get one from: https://console.groq.com
GROQ_API_KEY = "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"

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# ------------------------------------------------------------
# SYSTEM PROMPT
# ------------------------------------------------------------
SYSTEM_PROMPT = """You are AI Universe, a highly intelligent, friendly, and professional AI assistant. 
You provide accurate, detailed, and well-structured responses. 
You can help with coding, research, business, education, creative writing, and general questions.
Always be helpful, respectful, and thorough in your answers."""

# ------------------------------------------------------------
# AI CHAT ROUTE
# ------------------------------------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    """
    POST /chat
    Request Body: { "message": "user message here" }
    Response: { "reply": "AI response here" }
    """
    try:
        # Get JSON data from request
        data = request.get_json()

        # Validate request data
        if not data:
            return jsonify({"reply": "No message received"}), 400

        # Extract user message
        user_message = data.get("message", "").strip()

        # Check if message is empty
        if not user_message:
            return jsonify({"reply": "No message received"}), 200

        # ----------------------------------------------------
        # GROQ AI API CALL
        # ----------------------------------------------------
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False
        )

        # Extract AI response
        ai_reply = chat_completion.choices[0].message.content

        # Return successful response
        return jsonify({"reply": ai_reply}), 200

    # ----------------------------------------------------
    # ERROR HANDLING
    # ----------------------------------------------------
    except Exception as e:
        # Log the error for debugging
        print(f"Server Error: {str(e)}")

        # Return error response to client
        return jsonify({"reply": f"Server Error: {str(e)}"}), 500


# ------------------------------------------------------------
# HEALTH CHECK ROUTE
# ------------------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "online",
        "message": "AI Universe Backend is running!",
        "endpoints": {
            "chat": "POST /chat"
        }
    }), 200


# ------------------------------------------------------------
# SERVER START
# ------------------------------------------------------------
if __name__ == "__main__":
    # Run Flask on all network interfaces (0.0.0.0) so it's accessible
    # from your frontend running on VS Code Live Server
    # Port 5000 is the default Flask port
    # debug=True enables auto-reload when code changes
    print("=" * 50)
    print("AI Universe Backend Server")
    print("=" * 50)
    print("Server running at: http://127.0.0.1:5000")
    print("Chat endpoint: POST http://127.0.0.1:5000/chat")
    print("Press CTRL+C to stop the server")
    print("=" * 50)

    app.run(
        host="0.0.0.0",   # Listen on all network interfaces
        port=5000,         # Default Flask port
        debug=True         # Auto-reload on code changes
    )