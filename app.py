import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# This is the API endpoint for OpenRouter
THIRD_PARTY_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# This is the name of the model you want to use
# Find the exact name on OpenRouter's website (e.g., "cognitivecomputations/dolphin-mistral-latest")
MODEL_NAME = "cognitivecomputations/dolphin-mistral-latest" 

# --- Your Main API Endpoint ---
@app.route('/api/chat', methods=['POST'])
def chat_handler():
    try:
        # 1. Get the user's prompt from the request
        data = request.json
        user_prompt = data.get('prompt')

        if not user_prompt:
            return jsonify({"error": "No prompt provided"}), 400

        # 2. Get your SECRET API key from Vercel's environment variables
        #    NEVER put your key directly in the code.
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

# A simple root route to check if your server is running
@app.route('/')
def home():
    return "Your Flask API is running on Vercel!"
