"""The single place where "HH:MM" text and minutes after midnight are converted."""

import re

_HHMM = re.compile(r"(\d{2}):(\d{2})")


def parse_hhmm(text):
    """Convert "HH:MM" to minutes after midnight, or return None if invalid.

    Accepts 00:00-23:59, plus "24:00" (= 1440, end of day).
    Surrounding whitespace is ignored. Business rules are NOT checked here.
    """
    if not isinstance(text, str):
        return None
    match = _HHMM.fullmatch(text.strip())
    if not match:
        return None
    hours, minutes = int(match.group(1)), int(match.group(2))
    if hours == 24 and minutes == 0:
        return 1440
    if hours > 23 or minutes > 59:
        return None
    return hours * 60 + minutes


def format_hhmm(minutes):
    """Convert minutes after midnight (0-1440) to "HH:MM"."""
    return f"{minutes // 60:02d}:{minutes % 60:02d}"
