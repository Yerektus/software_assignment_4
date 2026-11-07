"""Minimal Flask web UI for the Room Availability Checker.

This layer only parses input, calls the domain functions and renders output.
All business rules live in booking.py, rooms.py and filtering.py.
"""

from flask import Flask, render_template, request

from booking import MAX_DURATION, check_room
from filtering import filter_rooms
from rooms import ROOMS
from timeutil import format_hhmm, parse_hhmm

NOW = 540  # Fixed "current time" (09:00) for this prototype.

# The ONE place where reason codes become user-facing text. None = allowed.
MESSAGES = {
    None: "Available: this room can be booked for that time.",
    "BLOCKED": "This room is blocked and cannot be booked.",
    "INVALID_RANGE": "End time must be after start time, on the same day.",
    "IN_PAST": f"Start time must be later than the current time ({format_hhmm(NOW)}).",
    "TOO_LONG": f"Booking cannot exceed {MAX_DURATION} minutes.",
    "OVERLAP": "This room is already booked during part of that time.",
}


def _parse_attendees(text):
    """Return a whole number >= 1, or None if the input is not one."""
    try:
        value = int(text)
    except (TypeError, ValueError):
        return None
    return value if value >= 1 else None


def create_app(rooms=ROOMS):
    """Build the app for a given room catalog (tests pass their own rooms)."""
    app = Flask(__name__)
    equipment_options = sorted({item for room in rooms for item in room.equipment})

    @app.get("/")
    def index():
        args = request.args
        form = {
            "attendees": args.get("attendees", "1"),
            "equipment": args.getlist("equipment"),
            "start": args.get("start", "").strip(),
            "end": args.get("end", "").strip(),
        }
        errors = []
        notice = None
        hint = None
        result = None

        attendees = _parse_attendees(form["attendees"])
        if attendees is None:
            errors.append("Attendees must be a whole number of at least 1.")
            matches = ()
        else:
            matches = filter_rooms(rooms, attendees, form["equipment"])

        # F5: only a room in the CURRENT filtered list can stay selected.
        room_id = args.get("room", "")
        selected = next((room for room in matches if room.id == room_id), None)
        if room_id and selected is None and not errors:
            notice = ("The room you selected no longer matches the filters, "
                      "so the selection was cleared.")

        # F5: the result is computed from this request only, for the selected room.
        if selected is not None:
            if not form["start"] or not form["end"]:
                hint = "Enter a start and end time to check this room."
            else:
                start, end = parse_hhmm(form["start"]), parse_hhmm(form["end"])
                if start is None or end is None:
                    errors.append("Start and end must be times in HH:MM format.")
                else:
                    reason = check_room(selected, start, end, NOW)
                    result = {
                        "ok": reason is None,
                        "message": MESSAGES[reason],
                        "room": selected.name,
                        "slot": f"{format_hhmm(start)}–{format_hhmm(end)}",
                    }
        elif matches and notice is None:
            hint = "Select a room and enter a start and end time, then press Check."

        return render_template(
            "index.html",
            now=format_hhmm(NOW),
            max_duration=MAX_DURATION,
            form=form,
            equipment_options=equipment_options,
            matches=matches,
            selected=selected,
            errors=errors,
            notice=notice,
            hint=hint,
            result=result,
            fmt=format_hhmm,
        )

    return app


app = create_app()
