"""Date handling utils."""

from datetime import datetime
from zoneinfo import ZoneInfo

from src.settings import config

TIMEZONE = config.get("timezone", "Europe/Madrid")


def utc_datetime(date_str: str, timezone: str = TIMEZONE) -> datetime:
    """Parse a date string and return a UTC date."""
    try:
        my_date = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
    except ValueError:
        try:
            my_date = datetime.strptime(date_str, "%d/%m/%Y %H:%M")
        except ValueError:
            try:
                my_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                my_date = datetime.strptime(date_str, "%d/%m/%Y")

    my_date_with_tz = my_date.replace(tzinfo=ZoneInfo(timezone))
    my_date_in_utc = my_date_with_tz.astimezone(ZoneInfo("UTC"))
    return my_date_in_utc


def format_time(my_date: datetime, timezone: str = TIMEZONE) -> str:
    """Format a datetime and return time in nice format."""
    my_date_with_tz = my_date.astimezone(ZoneInfo(timezone))
    return my_date_with_tz.time().strftime("%H:%M")


def date_timestamp(my_datetime: datetime, timezone: str = TIMEZONE) -> int:
    """Return timestamp for the date part of a datetime."""
    my_datetime_with_tz = my_datetime.astimezone(ZoneInfo(timezone))
    my_date = my_datetime_with_tz.replace(hour=0, minute=0, second=0, microsecond=0)
    return int(my_date.timestamp())
