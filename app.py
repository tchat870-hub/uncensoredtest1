import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# --- API Details ---
THIRD_PARTY_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "mistralai/mistral-7b-instruct:free" 


# --- NEW: Route to serve the HTML chat page ---
@app.route('/')
def home():
    # This line tells Flask to find 'index.html' in the same directory ('.')
    # and send it to the user's browser.
    return send_from_directory('.', 'index.html')


# --- Your API Endpoint (this code is the same) ---
@app.route('/api/chat', methods=['POST'])
def chat_handler():
    try:
        # 1. Get the user's prompt
        data = request.json
        user_prompt = data.get('prompt')

        if not user_prompt:
            return jsonify({"error": "No prompt provided"}), 400

        # 2. Get your SECRET API key from Vercel's environment variables
        api_key = os.environ.get("MY_SECRET_API_KEY")
        if not api_key:
            return jsonify({"error": "API key not configured"}), 500

        # 3. Set up the request to the third-party API
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "user", "content": user_prompt}
            ]
        }

        # 4. Make the call to the third-party API
        response = requests.post(THIRD_PARTY_API_URL, headers=headers, json=payload)
        
        # Check if the third-party call was successful
        response.raise_for_status() 

        # 5. Get the AI's response and send it back to your user
        ai_response = response.json()
        return jsonify(ai_response)

    except requests.exceptions.RequestException as e:
        # Handle errors from the third-party API
        return jsonify({"error": f"API request failed: {e}"}), 502
    except Exception as e:
        # Handle other unexpected errors
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

# --- NEW: Add a handler for favicon.ico ---
# Browsers automatically ask for this icon; this stops a 404 error in your logs
@app.route('/favicon.ico')
def favicon():
    return '', 204
