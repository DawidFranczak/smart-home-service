from fastapi import FastAPI

from app.lifespan import startup_event
from app.router.dummy import router as dummy_router
from app.router.temperature import router as temperature_router
from app.router.humidity import router as humidity_router

app = FastAPI(lifespan=startup_event)

app.include_router(dummy_router)
app.include_router(temperature_router)
app.include_router(humidity_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
