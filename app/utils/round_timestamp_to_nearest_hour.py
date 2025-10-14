from datetime import datetime

def round_timestamp_to_nearest_hour() -> datetime:
    """
    Returns the current time rounded to the nearest hour.
    If the current minute is greater than 30, rounds up to the next hour.

    Returns:
        datetime: The rounded timestamp with minutes, seconds, and microseconds set to 0.
    """
    timestamp = datetime.now()
    if timestamp.minute > 30:
        timestamp = timestamp.replace(hour=timestamp.hour + 1)
    return timestamp.replace(minute=0, second=0, microsecond=0)