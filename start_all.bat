@echo off
echo Starting Flask proxy...
start cmd /k "python proxy.py"

timeout /t 5 /nobreak > NUL

echo Starting Ngrok on port 12345...
start cmd /k "ngrok.exe http 12345"
