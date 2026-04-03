from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.lifespan import startup_event
from app.router.dummy import router as dummy_router
from app.router.measurement import router as measurement_router

origins = ["http://localhost:5173"]
app = FastAPI(lifespan=startup_event)
app.include_router(dummy_router)
app.include_router(measurement_router, prefix="/sensor/api/v1")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
