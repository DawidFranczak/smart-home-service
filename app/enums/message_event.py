from enum import Enum


class MessageEvent(str, Enum):
    ON_MEASURE_TEMPERATURE = "on_measure_temp"
    ON_MEASURE_HUMIDITY = "on_measure_hum"
    ON_MEASUREMENT_TEMP_HUM = "on_measurement_temp_hum"
