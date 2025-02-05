from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Load Webex Token from environment variables
WEBEX_ACCESS_TOKEN = os.getenv("WEBEX_ACCESS_TOKEN")
WEBEX_CALLING_API_URL = "https://webexapis.com/v1/telephony/calls"
WEBEX_FROM_NUMBER = os.getenv("WEBEX_FROM_NUMBER")  # Your Webex assigned number
TARGET_EXTENSION = "1005"  # Replace with your internal Webex extension

# Text-to-Speech (TTS) Message (This is what the call will say)
TTS_MESSAGE = "Attention! Motion has been detected in the server room. Please check immediately."

# Function to convert text to speech (TTS) using Webex Calling API
def initiate_webex_call():
    headers = {
        "Authorization": f"Bearer {WEBEX_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "destination": TARGET_EXTENSION,
        "from": WEBEX_FROM_NUMBER,
        "message": TTS_MESSAGE  # This message will be spoken when the call is answered
    }

    response = requests.post(WEBEX_CALLING_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        return {"status": "Call triggered successfully", "response": response.json()}
    else:
        return {"status": "Call failed", "error": response.text}

@app.route("/")
def home():
    return "Webhook Receiver for Meraki & Webex Calls", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json  # Incoming data from Meraki
    print("Received Meraki Webhook:", data)

    # Check if the alert is from a motion sensor activation
    if data.get("alertType") == "motion_detected":
        response = initiate_webex_call()
        return jsonify(response)
    
    return jsonify({"status": "No action taken"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
