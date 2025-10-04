from fastapi import FastAPI

from app.lifespan import startup_event

app = FastAPI(lifespan=startup_event)


@app.get("/")
async def root():
    return {"message": "Hello World"}