from datetime import datetime, timezone
from zoneinfo import ZoneInfo


LOCAL_TIMEZONE = ZoneInfo("America/Sao_Paulo")


def format_database_timestamp(value):
    """Convert a SQLite UTC timestamp into the local Brazilian time."""
    if not value:
        return ""
    try:
        timestamp = datetime.fromisoformat(str(value).replace(" ", "T"))
    except ValueError:
        return str(value)
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    return timestamp.astimezone(LOCAL_TIMEZONE).strftime("%d/%m %H:%M BRT")
