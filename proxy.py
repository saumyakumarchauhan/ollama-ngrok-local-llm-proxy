from flask import Flask, request, Response
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Target URL (your Ollama local server)
OLLAMA_URL = "http://localhost:11434"

# Email header to add
X_EMAIL = "24f1000666@ds.study.iitm.ac.in"

@app.route('/', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def proxy(path):
    # Construct target URL
    url = f"{OLLAMA_URL}/{path}"

    # Clone incoming headers and add required ones
    headers = dict(request.headers)
    headers['X-Email'] = X_EMAIL
    headers['Host'] = 'localhost:11434'  # optional, sometimes necessary

    # Forward the request to Ollama
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            params=request.args,
            timeout=10
        )
    except requests.exceptions.RequestException as e:
        return Response(f"Error connecting to Ollama: {str(e)}", status=502)

    # Filter response headers
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    response_headers = [(name, value) for (name, value) in resp.raw.headers.items()
                        if name.lower() not in excluded_headers]

    # Log for debugging
    print(f"\n Request to: {url}")
    print(f" Status: {resp.status_code}")
    print(f" Response headers: {resp.headers}")
    try:
        print(f"Response content: {resp.content.decode('utf-8')}")
    except:
        print(" Response content (non-text):", resp.content)

    # Send back response
    return Response(resp.content, resp.status_code, response_headers)

if __name__ == '__main__':
    app.run(port=12345)
