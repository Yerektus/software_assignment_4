"""Room availability check (AC1-AC4). Standard library only."""

DAY_END = 1440
MAX_DURATION = 120


def can_book(start, end, now, blocked, existing):
    """Return True only if the request satisfies AC1-AC4, else False.

    start, end, now: integer minutes after midnight.
    blocked: True if the room is blocked (AC3).
    existing: list of (b_start, b_end) pairs, in any order.

    Inputs are only read, never modified. Type checking is the caller's job.
    """
    # AC3: a blocked room rejects every request.
    if blocked:
        return False

    # AC1: valid range and order (also rejects reversed, zero length, negatives).
    if not (0 <= start < end <= DAY_END):
        return False

    # AC1: start must be strictly after now.
    if not start > now:
        return False

    # AC2: at most 120 minutes (exactly 120 is allowed).
    if end - start > MAX_DURATION:
        return False

    # AC4: reject overlap with ANY booking. Touching at an endpoint is fine.
    for b_start, b_end in existing:
        if start < b_end and end > b_start:
            return False

    return True