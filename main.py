from fastapi import FastAPI, Request
import requests

app = FastAPI()
VERIFY_TOKEN = "your_verification_token"

@app.get("/webhook")
async def verify_webhook(mode: str = None, token: str = None, challenge: str = None):
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)
    return "Forbidden", 403

@app.post("/webhook")
async def handle_message(request: Request):
    data = await request.json()
    for entry in data.get("entry", []):
        for message_event in entry.get("messaging", []):
            sender_id = message_event["sender"]["id"]
            if "message" in message_event:
                send_message(sender_id, "Hello! This is a bot response.")
    return "ok"

def send_message(recipient_id, text):
    params = {"access_token": "your_page_access_token"}
    payload = {"recipient": {"id": recipient_id}, "message": {"text": text}}
    requests.post("https://graph.facebook.com/v17.0/me/messages", params=params, json=payload)