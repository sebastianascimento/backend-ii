from fastapi import FastAPI

api = FastAPI()

@api.get("/")
def index():
    return "Hello, World!"


@api.post("/pay")
def process_payment(method: str):
    match method.lower():
        