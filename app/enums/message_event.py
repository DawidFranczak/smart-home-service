from enum import Enum


class MessageEvent(str, Enum):
    ON_MEASURE_TEMPERATURE = "on_measure_temperature"
    ON_MEASURE_HUMIDITY = "on_measure_humidity"
    STATE_CHANGE = "state_change"
