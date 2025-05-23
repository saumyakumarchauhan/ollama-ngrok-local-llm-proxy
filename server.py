from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt', '')
    print(f"Received prompt: {prompt}")  # Log prompt

    try:
        result = subprocess.run(
            ["ollama", "run", "gemma3:1b-it-qat", prompt],
            capture_output=True, text=True, check=True,
            timeout=10  # prevent infinite hang
        )
        response = result.stdout.strip()
        print(f"Ollama response: {response}")  # Log response
        return jsonify({"response": response})
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Ollama command timed out"}), 504
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to get response from Ollama", "details": str(e)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
