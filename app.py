import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Replace with your actual OpenRouter API key
OPENROUTER_API_KEY = "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"

# Home page with UI
@app.route('/')
def index():
    return render_template('index.html')

# Chat route for API
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Message is required!"}), 400

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            reply = result["choices"][0]["message"]["content"]
            return jsonify({"response": reply})
        else:
            return jsonify({"error": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
