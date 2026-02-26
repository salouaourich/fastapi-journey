from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def root():
    return {"message": "Greetings from your FastAPI spaceship!"}
