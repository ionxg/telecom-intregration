from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

sessions = {}

@app.get("/")
def root():
    return {"message": "Session Service is running"}

@app.post("/session/{subscriber_id}")
def create_session(subscriber_id: str):
    try:
        response = requests.get(f"http://127.0.0.1:8000/subscriber/{subscriber_id}")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=500, detail="Subscriber Service is unavailable")

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Subscriber not found")

    subscriber = response.json()

    if subscriber["status"] != "active":
        raise HTTPException(status_code=400, detail="Subscriber is not active")

    if not subscriber["volte_enabled"]:
        raise HTTPException(status_code=400, detail="VoLTE is not enabled")

    session = {
        "subscriber_id": subscriber_id,
        "session_status": "created"
    }

    sessions[subscriber_id] = session
    return {
        "message": "Session created successfully",
        "session": session
    }

@app.get("/session/{subscriber_id}")
def get_session(subscriber_id: str):
    session = sessions.get(subscriber_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return session