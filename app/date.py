from datetime import datetime, timezone


def fromtimestamp(timestamp):
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)


def now():
    return datetime.now(tz=timezone.utc)
