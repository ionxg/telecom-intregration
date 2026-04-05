# Voice Service: checks active sessions and simulates VoLTE call setup

from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

calls = {}

@app.get("/")
def root():
    return {"message": "Voice Service is running"}

@app.post("/call/{subscriber_id}")
def create_call(subscriber_id: str):
    try:
        response = requests.get(f"http://127.0.0.1:8001/session/{subscriber_id}")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=500, detail="Session Service is unavailable")

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="No active session for subscriber")

    call = {
        "subscriber_id": subscriber_id,
        "call_status": "connected"
    }

    calls[subscriber_id] = call

    return {
        "message": "Call created successfully",
        "call": call
    }

@app.get("/call/{subscriber_id}")
def get_call(subscriber_id: str):
    call = calls.get(subscriber_id)

    if not call:
        raise HTTPException(status_code=404, detail="Call not found")

    return call