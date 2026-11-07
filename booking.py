"""Room availability check (AC1-AC4). Standard library only."""

DAY_END = 1440
MAX_DURATION = 120


def check_booking(start, end, now, blocked, existing):
    """Return None if the request satisfies AC1-AC4, else the first failing
    reason code: "BLOCKED", "INVALID_RANGE", "IN_PAST", "TOO_LONG", "OVERLAP".

    start, end, now: integer minutes after midnight.
    blocked: True if the room is blocked (AC3).
    existing: list of (b_start, b_end) pairs, in any order.

    Inputs are only read, never modified. Type checking is the caller's job.
    """
    # AC3: a blocked room rejects every request.
    if blocked:
        return "BLOCKED"

    # AC1: valid range and order (also rejects reversed, zero length, negatives).
    if not (0 <= start < end <= DAY_END):
        return "INVALID_RANGE"

    # AC1: start must be strictly after now.
    if not start > now:
        return "IN_PAST"

    # AC2: at most 120 minutes (exactly 120 is allowed).
    if end - start > MAX_DURATION:
        return "TOO_LONG"

    # AC4: reject overlap with ANY booking. Touching at an endpoint is fine.
    for b_start, b_end in existing:
        if start < b_end and end > b_start:
            return "OVERLAP"

    return None


def can_book(start, end, now, blocked, existing):
    """Return True only if the request satisfies AC1-AC4, else False."""
    return check_booking(start, end, now, blocked, existing) is None


def check_room(room, start, end, now):
    """Like check_booking, using this room's own blocked flag and bookings."""
    return check_booking(start, end, now, room.blocked, room.bookings)