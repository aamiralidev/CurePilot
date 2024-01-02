from fastapi import FastAPI

app = FastAPI()


@app.get("/codegpt")
async def get_data():
    data = {"message": "Welcome to Code GPT!"}
    return data


@app.post("/codegpt")
async def process_data(data: dict):
    return {"response": "This is a response from Code GPT!"}
