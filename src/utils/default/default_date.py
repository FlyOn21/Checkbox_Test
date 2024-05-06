from datetime import datetime


def default_end_date():
    now = datetime.utcnow().date()
    if now.month == 12:
        return datetime(now.year + 1, 1, 1).date()
    else:
        return datetime(now.year, now.month + 1, 1).date()


def default_start_date():
    return datetime.utcnow().date().replace(day=1)
