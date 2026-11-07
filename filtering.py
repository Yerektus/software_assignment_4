"""Room search filters (F1, F2, F4). Standard library only."""


def filter_rooms(rooms, attendees, equipment):
    """Return a tuple of the rooms that fit the request, in catalog order.

    F1: room.capacity >= attendees.
    F2: room has ALL items in `equipment` (empty selection matches every room).
    F4: returns an empty tuple when nothing matches.

    Does not check blocked status or time; use booking.check_room for that.
    Inputs are only read, never modified.
    """
    required = set(equipment)
    return tuple(
        room for room in rooms
        if room.capacity >= attendees and required <= set(room.equipment)
    )
