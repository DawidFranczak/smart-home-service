from datetime import datetime, timedelta


def fill_default_date_range(
    start_date: datetime | None, end_date: datetime | None
) -> tuple[datetime, datetime]:
    if not start_date and not end_date:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
    elif not end_date:
        end_date = start_date + timedelta(days=7)
    elif not start_date:
        start_date = end_date - timedelta(days=7)
    else:
        end_date += timedelta(days=1)

    return start_date, end_date
