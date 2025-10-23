from fastapi import APIRouter
from time import time
from datetime import datetime, timedelta
import random
from app.db.connection import SessionDB
from app.models.measurement import HumidityMeasurement, TemperatureMeasurement

router = APIRouter(prefix="/dummy", tags=["dummy"])


@router.get("/temp_hum")
async def dummy_temp_hum(db: SessionDB):
    start_time = time()
    mac = "48:3F:DA:45:23:69"
    temp_max = 40
    temp_min = -20
    hum_max = 100
    hum_min = 10
    start_date = datetime(2025, 1, 1, hour=0, minute=0, second=0)
    end_date = datetime(2025, 12, 30, hour=23, minute=0, second=0)
    hum_list = []
    tem_list = []
    new_hum = random.uniform(hum_min, hum_max)
    new_temp = random.randint(temp_min, temp_max)
    while start_date <= end_date:
        new_hum += random.uniform(-3.0, 3.0)
        new_temp += random.uniform(-1.0, 1.0)
        new_temp = max(min(new_temp, temp_max), temp_min)
        new_hum = max(min(new_hum, hum_max), hum_min)
        hum_list.append(
            HumidityMeasurement(
                sensor_id=mac,
                value=round(new_hum, 2),
                timestamp=start_date,
            )
        )
        tem_list.append(
            TemperatureMeasurement(
                sensor_id=mac,
                value=round(new_temp, 2),
                timestamp=start_date,
            )
        )
        start_date += timedelta(hours=1)
    db.add_all(hum_list)
    db.add_all(tem_list)
    # await db.commit()
    return {"status": "ok", "time": time() - start_time}
