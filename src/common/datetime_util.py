import time
from datetime import datetime, timedelta, timezone


DT_AWARE = "%m/%d/%y %I:%M:%S %p %Z"
DT_NAIVE = "%m/%d/%y %I:%M:%S %p"


def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0)


def localized_dt_string(dt, use_tz=None):
    if not dt.tzinfo and not use_tz:
        return dt.strftime(DT_NAIVE)
    if not dt.tzinfo:
        return dt.replace(tzinfo=use_tz).strftime(DT_AWARE)
    return (
        dt.astimezone(use_tz).strftime(DT_AWARE)
        if use_tz
        else dt.strftime(DT_AWARE)
    )


def get_local_utcoffset():
    utc_offset = timedelta(seconds=time.localtime().tm_gmtoff)
    return timezone(offset=utc_offset)


def make_tzaware(dt, use_tz=None, localize=True):
    if not use_tz:
        use_tz = get_local_utcoffset()
    return dt.astimezone(use_tz) if localize else dt.replace(tzinfo=use_tz)
