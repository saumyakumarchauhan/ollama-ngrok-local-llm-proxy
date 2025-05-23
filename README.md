# Ollama Chat API + Proxy + Ngrok Tunnel

This project exposes a local Ollama instance through a Flask-based API, adds header-based authentication using a proxy, and makes the service accessible over the internet via Ngrok. It's ideal for internal AI diagnostics, Google OAuth restriction, or frontend integration.

## 📁 Project Structure

```
.
├── app.py              # Main API to query Ollama using /chat
├── proxy.py            # CORS-enabled proxy to inject X-Email header
├── server.py           # CLI-based backend using subprocess for ollama run
├── start_alal.bat      # Starts proxy and Ngrok tunnel
├── requirements.txt    # Python dependencies
```
---

## 🔧 Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Enable CORS for Ollama

In a terminal running Ollama, set the following:

```bash
export OLLAMA_ORIGINS="*"
ollama serve
```

### 3. Ngrok Setup

#### a. Get an Ngrok Authtoken

- Go to https://dashboard.ngrok.com
- Sign in and copy your authtoken
- Run:

```bash
ngrok config add-authtoken YOUR_AUTHTOKEN
```

#### b. Expose Ollama Securely

```bash
ngrok http 11434 \
  --response-header-add "X-Email: 24f1000666@ds.study.iitm.ac.in" \
  --response-header-add "Access-Control-Expose-Headers: *" \
  --response-header-add "Access-Control-Allow-Headers: Authorization,Content-Type,User-Agent,Accept,Ngrok-skip-browser-warning"
```

Save the forwarding URL Ngrok prints (e.g., https://abcd1234.ngrok-free.app).

### ✅ Verify Setup

Using curl:

```bash
curl -X POST https://abcd1234.ngrok-free.app/api/chat \
  -H "Content-Type: application/json" \
  -H "X-Email: 24f1000666@ds.study.iitm.ac.in" \
  -d '{"prompt": "What is the capital of France?"}'
```

Response should include:

- Header: `Access-Control-Allow-Origin: *`
- Echoed `X-Email` header
- JSON body like:
```json
{"response": "The capital of France is Paris."}
```

## 🧠 API Overview

### /chat (POST)

Queries Ollama using the specified model (`gemma3:1b-it-qat`).

**Request:**
```json
{
  "prompt": "Tell me a joke."
}
```

**Response:**
```json
{
  "response": "Why did the chicken join a band? Because it had the drumsticks!"
}
```

## 🔄 Start Everything via start_alal.bat

```bat
@echo off
start cmd /k "python proxy.py"
timeout /t 5 /nobreak > NUL
start cmd /k "ngrok.exe http 12345"
```

This starts the Flask proxy and then launches Ngrok on port 12345.

## 🧪 Advanced Use (OAuth, User Agents)

Restrict to specific Google users:

```bash
ngrok http 11434 \
  --oauth google \
  --oauth-client-id $CLIENT_ID \
  --oauth-client-secret $SECRET \
  --oauth-allow-domain iitm.ac.in \
  --oauth-allow-email 24f1000666@ds.study.iitm.ac.in
```

Block bots:

```bash
--ua-filter-deny ".*bot$"
```

## 📌 Notes

- Make sure Ollama is running on `localhost:11434`
- The proxy (port `12345`) injects the required `X-Email` header for validation
- Use the Ngrok HTTPS URL (e.g., `https://abcd1234.ngrok-free.app`) for frontend/API clients

## 📄 License

MIT License

Made with ❤️ by 24f1000666@ds.study.iitm.ac.in