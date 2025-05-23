from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Ollama Chat API is running. Use POST /chat with JSON to interact."

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt', '')

    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "gemma3:1b-it-qat",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            },
            stream=True,
            timeout=30
        )

        final_response = ""

        for line in response.iter_lines():
            if line:
                try:
                    json_line = json.loads(line.decode('utf-8'))
                    if "message" in json_line and "content" in json_line["message"]:
                        final_response += json_line["message"]["content"]
                except json.JSONDecodeError:
                    continue

        return jsonify({"response": final_response})

    except requests.exceptions.Timeout:
        return jsonify({"error": "Ollama request timed out"}), 504
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
