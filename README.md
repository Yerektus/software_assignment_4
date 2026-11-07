# Smart Campus Room Availability Checker

A small Flask web page for checking whether a campus room can be booked for a time
slot on a single day. You filter rooms by number of attendees and required equipment,
pick a room and enter a start and end time. The page then shows either that the room
is available or the reason it is not.

This is a prototype. All data is fictional, and it has no database, login, payments
or live APIs.

## Project structure

| File | Responsibility |
|---|---|
| `booking.py` | Booking rules. `check_booking` returns `None` (allowed) or a reason code, `can_book` returns True/False, and `check_room` applies the rules to one `Room`. |
| `rooms.py` | The frozen `Room` dataclass and the fictional `ROOMS` catalog. |
| `filtering.py` | `filter_rooms`: keeps rooms with enough capacity and all of the selected equipment. |
| `timeutil.py` | Converts between `HH:MM` text and minutes after midnight. |
| `app.py` | Flask web layer. Parses the form, calls the functions above, maps reason codes to messages (`MESSAGES`) and renders the page. Contains no business rules. |
| `templates/index.html` | The single page: filters, time inputs, room list and result. |
| `static/style.css` | Plain CSS. Responsive at phone width, with dark mode. |
| `test_booking.py` | Tests for the booking rules (AC1–AC5) and the reason codes, including rule priority. |
| `test_rooms.py` | Tests for the catalog, `filter_rooms` and `check_room` (F1–F4, per-room bookings). |
| `test_timeutil.py` | Tests for time parsing and formatting. |
| `test_app.py` | Integration tests for the web page using Flask's `test_client()`. |
| `test_results.txt` | Saved output of a full test run. |
| `requirements.txt` | Python dependency: `flask`. |

## Rules

The booking rules in `booking.py` are checked in this order. The first one that fails
gives the reason code.

| Code | Rule | Message shown on the page |
|---|---|---|
| `BLOCKED` | A blocked room can never be booked (AC3). | This room is blocked and cannot be booked. |
| `INVALID_RANGE` | End must be after start, within 00:00–24:00 (AC1). | End time must be after start time, on the same day. |
| `IN_PAST` | Start must be later than the current time (AC1). | Start time must be later than the current time (09:00). |
| `TOO_LONG` | At most 120 minutes; exactly 120 is allowed (AC2). | Booking cannot exceed 120 minutes. |
| `OVERLAP` | Must not overlap an existing booking of that room. Touching end to end is allowed (AC4). | This room is already booked during part of that time. |

If every rule passes, the page shows "Available: this room can be booked for that time."

The checks only read their inputs and never modify bookings (AC5). Rooms are frozen
dataclasses with tuple fields.

The room filters live in `filtering.py` and `app.py`:
- **F1:** a room's capacity must be at least the number of attendees.
- **F2:** a room must have all of the selected equipment.
- **F3:** a blocked room may appear in the list, marked with a "Blocked" badge, but it is never reported as available.
- **F4:** when no rooms match, the page shows "No rooms match these filters".
- **F5:** the result is always computed from the current request for the selected room. If the selected room no longer matches the filters, the selection and the result are cleared. Choosing a different room submits the form automatically. The **Check** button still works when JavaScript is disabled.

## Setup

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```sh
flask --app app run
```

Then open http://127.0.0.1:5000.

## Tests

```sh
python3 -m unittest discover -v
```

Run the tests with the virtual environment active, because `test_app.py` needs Flask.

## Fixed current time

The app uses a fixed current time, `NOW = 540` in `app.py`, which is **09:00**. It is
shown on the page. Bookings must start after 09:00. The functions in `booking.py`
take `now` as a parameter and never read the system clock.

## Room catalog (fictional)

Defined in `rooms.py`:

| ID | Name | Capacity | Equipment | Blocked | Existing bookings |
|---|---|---|---|---|---|
| A101 | Aurora Seminar Room | 12 | whiteboard | no | 10:00–11:00, 13:00–14:00 |
| B202 | Birch Lecture Hall | 60 | projector, whiteboard | no | 11:00–13:00 |
| C303 | Cedar Meeting Pod | 6 | video_conf | no | none |
| D404 | Dune Media Lab | 20 | projector, video_conf, whiteboard | **yes** | none |

## Git tags

| Tag | Meaning |
|---|---|
| `baseline` | The Assignment #03 prototype before any changes. It had two identical modules (`booking.py`, `booking_v1.py`) and three test files. |
| `final` | The finished version, with the Flask UI and the full test suite. |

```sh
git diff --stat baseline final   # summary of everything that changed
git checkout baseline            # inspect the original prototype
git checkout main                # return to the latest version
```
