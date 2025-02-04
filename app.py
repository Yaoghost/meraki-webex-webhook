from flask import Flask, request, jsonify
import requests
import os
app = Flask(__name__)

# Webex API settings
WEBEX_ACCESS_TOKEN = os.getenv("WEBEX_ACCESS_TOKEN")
WEBEX_CALLING_API_URL = "https://webexapis.com/v1/telephony/calls"
TARGET_EXTENSION = "1005"  # Replace with the internal Webex extension to call

# Function to trigger Webex Call API
def initiate_webex_call():
    headers = {
        "Authorization": f"Bearer {WEBEX_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "destination": TARGET_EXTENSION,  # Webex extension to call
        "from": "YOUR_WEBEX_NUMBER",  # Your Webex assigned number
        "message": "🚨 Sensor Alert: Motion detected!"
    }
    
    response = requests.post(WEBEX_CALLING_API_URL, json=payload, headers=headers)
    return response.json()

@app.route("/")
def home():
    return "Webhook Receiver for Meraki & Webex Calls", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json  # Incoming data from Meraki
    print("Received Meraki Webhook:", data)
    
    # Check if the alert is from a sensor activation
    if data.get("alertType") == "motion_detected":
        response = initiate_webex_call()
        return jsonify({"status": "call triggered", "response": response})
    
    return jsonify({"status": "no action taken"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
