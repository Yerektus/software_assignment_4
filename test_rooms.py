import dataclasses
import unittest

from booking import check_room
from filtering import filter_rooms
from rooms import ROOMS, Room

NOW = 540

# Local fixtures, so tests do not break when the fictional catalog changes.
SMALL = Room("T1", "Test Small", 10, ("projector", "whiteboard"), False, ((600, 660),))
LARGE = Room("T2", "Test Large", 40, ("whiteboard",), False, ())
LOCKED = Room("T3", "Test Locked", 40, ("projector",), True, ())


class TestCatalog(unittest.TestCase):
    def test_catalog_has_four_rooms_one_blocked_and_varied_equipment(self):
        self.assertGreaterEqual(len(ROOMS), 4)
        self.assertTrue(any(room.blocked for room in ROOMS))
        self.assertGreater(len({room.equipment for room in ROOMS}), 1)

    def test_room_is_frozen(self):
        with self.assertRaises(dataclasses.FrozenInstanceError):
            SMALL.blocked = True


class TestF1Capacity(unittest.TestCase):
    def test_f1_exact_capacity_is_included(self):
        self.assertIn(SMALL, filter_rooms((SMALL,), 10, ()))

    def test_f1_capacity_one_below_attendees_is_excluded(self):
        self.assertNotIn(SMALL, filter_rooms((SMALL,), 11, ()))


class TestF2Equipment(unittest.TestCase):
    def test_f2_room_with_all_selected_equipment_is_included(self):
        self.assertIn(SMALL, filter_rooms((SMALL,), 1, ("projector", "whiteboard")))

    def test_f2_room_missing_one_selected_item_is_excluded(self):
        self.assertNotIn(SMALL, filter_rooms((SMALL,), 1, ("projector", "video_conf")))


class TestF3Blocked(unittest.TestCase):
    def test_f3_blocked_room_is_never_available(self):
        for start, end in [(541, 600), (660, 720), (1380, 1440)]:
            self.assertEqual(check_room(LOCKED, start, end, NOW), "BLOCKED")

    def test_f3_blocked_catalog_rooms_are_never_available(self):
        for room in ROOMS:
            if room.blocked:
                self.assertEqual(check_room(room, 900, 960, NOW), "BLOCKED")


class TestF4NoMatches(unittest.TestCase):
    def test_f4_no_matches_returns_empty_tuple(self):
        self.assertEqual(filter_rooms((SMALL, LARGE, LOCKED), 100, ()), ())

    def test_f4_result_is_always_a_tuple(self):
        self.assertIsInstance(filter_rooms([SMALL, LARGE], 1, ()), tuple)


class TestPerRoomBookings(unittest.TestCase):
    def test_same_slot_free_in_one_room_overlap_in_another(self):
        self.assertIsNone(check_room(LARGE, 620, 650, NOW))
        self.assertEqual(check_room(SMALL, 620, 650, NOW), "OVERLAP")


if __name__ == "__main__":
    unittest.main()
