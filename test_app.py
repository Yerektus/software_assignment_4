"""Integration tests for the Flask web layer, using app.test_client()."""

import unittest

from app import MESSAGES, create_app
from rooms import Room

# Local fixtures, so these tests do not depend on the fictional catalog.
ALPHA = Room("A", "Alpha Room", 10, ("projector", "whiteboard"), False, ())
BETA = Room("B", "Beta Room", 10, ("projector",), False, ((600, 660),))
GAMMA = Room("C", "Gamma Lab", 30, ("projector", "video_conf"), True, ())
DELTA = Room("D", "Delta Pod", 4, ("whiteboard",), False, ())
TEST_ROOMS = (ALPHA, BETA, GAMMA, DELTA)

ALL_RESULT_MESSAGES = tuple(MESSAGES.values())


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = create_app(rooms=TEST_ROOMS).test_client()

    def get(self, **params):
        response = self.client.get("/", query_string=params)
        self.assertEqual(response.status_code, 200)
        return response.get_data(as_text=True)


class TestPage(AppTestCase):
    def test_page_shows_fixed_current_time(self):
        self.assertIn("09:00", self.get())

    def test_equipment_checkboxes_come_from_room_data(self):
        body = self.get()
        for item in ("projector", "whiteboard", "video_conf"):
            self.assertIn(f'value="{item}"', body)


class TestFiltering(AppTestCase):
    def test_filter_shows_only_matching_rooms(self):
        body = self.get(attendees=8, equipment=["projector", "whiteboard"])
        self.assertIn("Alpha Room", body)
        for name in ("Beta Room", "Gamma Lab", "Delta Pod"):
            self.assertNotIn(name, body)

    def test_capacity_filter_excludes_small_room(self):
        body = self.get(attendees=5)
        self.assertNotIn("Delta Pod", body)
        self.assertIn("Alpha Room", body)

    def test_f4_empty_state_when_nothing_matches(self):
        body = self.get(attendees=100)
        self.assertIn("No rooms match these filters", body)
        for room in TEST_ROOMS:
            self.assertNotIn(room.name, body)

    def test_invalid_attendees_shows_error(self):
        body = self.get(attendees="zero")
        self.assertIn("Attendees must be a whole number", body)


class TestResult(AppTestCase):
    def test_f5_same_slot_available_in_room_a_overlap_in_room_b(self):
        slot = {"attendees": 2, "start": "10:20", "end": "10:50"}
        body_a = self.get(room="A", **slot)
        self.assertIn(MESSAGES[None], body_a)
        self.assertNotIn(MESSAGES["OVERLAP"], body_a)

        body_b = self.get(room="B", **slot)
        self.assertIn(MESSAGES["OVERLAP"], body_b)
        self.assertNotIn(MESSAGES[None], body_b)

    def test_f3_blocked_room_matching_filters_shows_blocked_message(self):
        body = self.get(attendees=20, equipment="video_conf", room="C",
                        start="10:00", end="11:00")
        self.assertIn("Gamma Lab", body)
        self.assertIn('class="badge">Blocked<', body)
        self.assertIn(MESSAGES["BLOCKED"], body)
        self.assertNotIn(MESSAGES[None], body)

    def test_f5_filtered_out_selection_clears_selection_and_result(self):
        # Delta Pod (capacity 4) was selected, then attendees changed to 8.
        body = self.get(attendees=8, room="D", start="10:00", end="11:00")
        self.assertIn("no longer matches the filters", body)
        self.assertNotIn("checked", body)
        for message in ALL_RESULT_MESSAGES:
            self.assertNotIn(message, body)

    def test_reason_code_is_shown_as_human_text(self):
        body = self.get(room="A", start="10:00", end="12:01")
        self.assertIn(MESSAGES["TOO_LONG"], body)
        self.assertNotIn("TOO_LONG", body)

    def test_bad_time_format_shows_error_and_no_result(self):
        body = self.get(room="A", start="10", end="11:00")
        self.assertIn("HH:MM", body)
        for message in ALL_RESULT_MESSAGES:
            self.assertNotIn(message, body)


if __name__ == "__main__":
    unittest.main()
