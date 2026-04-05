from fastapi import FastAPI

app = FastAPI()

subscribers = {
    "1001": {
        "subscriber_id": "1001",
        "msisdn": "0210000001",
        "status": "active"
    },
    "1002": {
        "subscriber_id": "1002",
        "msisdn": "0210000002",
        "status": "inactive"
    }
}

@app.get("/")
def root():
    return {"message": "Subscriber Service is running"}

@app.get("/subscriber/{subscriber_id}")
def get_subscriber(subscriber_id: str):
    subscriber = subscribers.get(subscriber_id)

    if subscriber:
        return subscriber

    return {"error": "Subscriber not found"}