"""Fictional room catalog. Standard library only."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Room:
    """One bookable room. Frozen, with tuple fields, so it cannot be modified (AC5).

    bookings: tuple of (start, end) pairs in minutes after midnight.
    """

    id: str
    name: str
    capacity: int
    equipment: tuple
    blocked: bool
    bookings: tuple


ROOMS = (
    Room("A101", "Aurora Seminar Room", 12, ("whiteboard",), False,
         ((600, 660), (780, 840))),
    Room("B202", "Birch Lecture Hall", 60, ("projector", "whiteboard"), False,
         ((660, 780),)),
    Room("C303", "Cedar Meeting Pod", 6, ("video_conf",), False,
         ()),
    Room("D404", "Dune Media Lab", 20, ("projector", "video_conf", "whiteboard"), True,
         ()),
)
