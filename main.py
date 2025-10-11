from fastapi import FastAPI

from app.lifespan import startup_event
from app.models.measurement import TemperatureMeasurement
from sqlmodel import select
from app.db.connection import SessionDB
app = FastAPI(lifespan=startup_event)


@app.get("/",response_model=list[TemperatureMeasurement])
async def root(db:SessionDB):
    result = await db.execute(select(TemperatureMeasurement))
    return result.scalars().all()