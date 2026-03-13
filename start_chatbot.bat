@echo off
REM Start Python HTTP Server and open chatbot UI in browser
cd /d "C:\Users\Admin\OneDrive\Desktop\Trainable ChatBot interface\examples"
start http://localhost:8080/chatbot_ui.html
python -m http.server 8080
