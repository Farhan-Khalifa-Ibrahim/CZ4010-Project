import datetime

epoch = datetime.datetime.utcfromtimestamp(0)


def to_timestamp(dt: datetime.datetime) -> float:
    """Returns the POSIX timestamp for the given datetime.

    Args:
        dt (datetime.datetime): The datetime to be converted.

    Returns:
        float: POSIX timestamp.
    """
    return dt.timestamp()


def from_timestamp(timestamp: float) -> datetime.datetime:
    """Returns the datetime object from the POSIX timestamp.

    Args:
        timestamp (float): The POSIX timestamp.

    Returns:
        datetime.datetime: The datetime.
    """
    return datetime.datetime.fromtimestamp(timestamp)


def current_timestamp() -> float:
    """Returns the timestamp for the current time.

    Returns:
        float: POSIX timestamp of the current time.
    """
    return to_timestamp(datetime.datetime.now())
