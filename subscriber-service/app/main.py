from fastapi import FastAPI, HTTPException

app = FastAPI()

subscribers = {
    "1001": {
        "subscriber_id": "1001",
        "msisdn": "0210000001",
        "status": "active",
        "volte_enabled": True
    },
    "1002": {
        "subscriber_id": "1002",
        "msisdn": "0210000002",
        "status": "inactive",
        "volte_enabled": False
    }
}

@app.get("/")
def root():
    return {"message": "Subscriber Service is running"}

@app.get("/subscriber/{subscriber_id}")
def get_subscriber(subscriber_id: str):
    subscriber = subscribers.get(subscriber_id)

    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")

    return subscriber

@app.post("/subscriber")
def create_subscriber(subscriber: dict):
    subscriber_id = subscriber.get("subscriber_id")

    if not subscriber_id:
        raise HTTPException(status_code=400, detail="subscriber_id is required")

    if subscriber_id in subscribers:
        raise HTTPException(status_code=400, detail="Subscriber already exists")

    subscribers[subscriber_id] = subscriber
    return {
        "message": "Subscriber created successfully",
        "subscriber": subscriber
    }