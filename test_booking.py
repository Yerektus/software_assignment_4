import copy
import unittest

from booking_v1 import can_book

NOW = 540
EXISTING = [(600, 660)]


def check(start, end, blocked=False, existing=None):
    if existing is None:
        existing = EXISTING
    return can_book(start, end, NOW, blocked, existing)


class TestAC1ValidTimes(unittest.TestCase):
    def test_ac1_start_equals_now_is_rejected(self):
        self.assertFalse(check(540, 570))

    def test_ac1_one_minute_after_now_is_allowed(self):
        self.assertTrue(check(541, 570))

    def test_ac1_reversed_times_are_rejected(self):
        self.assertFalse(check(700, 650))

    def test_ac1_zero_length_is_rejected(self):
        self.assertFalse(check(700, 700))

    def test_ac1_end_exactly_at_day_end_is_allowed(self):
        self.assertTrue(check(1380, 1440))

    def test_ac1_past_day_end_is_rejected(self):
        self.assertFalse(check(1400, 1441))


class TestAC2Duration(unittest.TestCase):
    def test_ac2_exactly_120_minutes_is_allowed(self):
        self.assertTrue(check(720, 840))

    def test_ac2_121_minutes_is_rejected(self):
        self.assertFalse(check(720, 841))


class TestAC3Blocked(unittest.TestCase):
    def test_ac3_blocked_room_rejects_valid_request(self):
        self.assertFalse(check(660, 720, blocked=True))


class TestAC4Overlap(unittest.TestCase):
    def test_ac4_touching_end_is_allowed(self):
        self.assertTrue(check(660, 720))

    def test_ac4_touching_start_is_allowed(self):
        self.assertTrue(check(541, 600))

    def test_ac4_one_minute_overlap_is_rejected(self):
        self.assertFalse(check(659, 700))

    def test_ac4_request_covering_booking_is_rejected(self):
        self.assertFalse(check(590, 670))

    def test_ac4_request_inside_booking_is_rejected(self):
        self.assertFalse(check(610, 650))

    def test_ac4_overlap_with_last_of_several_is_rejected(self):
        existing = [(600, 660), (700, 760), (900, 960)]
        self.assertFalse(check(930, 950, existing=existing))

    def test_ac4_overlap_with_later_booking_in_unsorted_list(self):
        existing = [(800, 860), (600, 660)]
        self.assertFalse(check(620, 650, existing=existing))

    def test_ac4_empty_bookings_allows_request(self):
        self.assertTrue(check(660, 720, existing=[]))

    def test_ac4_partial_overlap_with_booking_is_rejected(self):
        self.assertFalse(check(630, 690))

    def test_ac4_overlap_with_second_of_two_bookings_is_rejected(self):
        existing = [(600, 660), (800, 860)]
        self.assertFalse(check(830, 900, existing=existing))


class TestAC5NoMutation(unittest.TestCase):
    def test_ac5_inputs_unchanged_and_result_is_bool(self):
        existing = [(800, 860), (600, 660), (900, 960)]  # unsorted on purpose
        before = copy.deepcopy(existing)
        for start, end in [(660, 720), (620, 650), (700, 650), (930, 950)]:
            result = can_book(start, end, NOW, False, existing)
            self.assertIsInstance(result, bool)
        self.assertEqual(existing, before)


if __name__ == "__main__":
    unittest.main()