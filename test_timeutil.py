import unittest

from timeutil import format_hhmm, parse_hhmm


class TestParseHHMM(unittest.TestCase):
    def test_valid_times(self):
        cases = {"00:00": 0, "09:00": 540, "10:20": 620, "23:59": 1439, "24:00": 1440}
        for text, minutes in cases.items():
            with self.subTest(text=text):
                self.assertEqual(parse_hhmm(text), minutes)

    def test_surrounding_whitespace_is_ignored(self):
        self.assertEqual(parse_hhmm(" 09:30 "), 570)

    def test_invalid_times_return_none(self):
        for text in ["", "9:00", "0900", "12:60", "24:01", "25:00", "ab:cd",
                     "-1:00", "09:00:00", "12:5"]:
            with self.subTest(text=text):
                self.assertIsNone(parse_hhmm(text))

    def test_non_string_returns_none(self):
        self.assertIsNone(parse_hhmm(None))
        self.assertIsNone(parse_hhmm(540))


class TestFormatHHMM(unittest.TestCase):
    def test_format(self):
        self.assertEqual(format_hhmm(0), "00:00")
        self.assertEqual(format_hhmm(540), "09:00")
        self.assertEqual(format_hhmm(1440), "24:00")

    def test_round_trip(self):
        for minutes in (0, 59, 540, 1439, 1440):
            with self.subTest(minutes=minutes):
                self.assertEqual(parse_hhmm(format_hhmm(minutes)), minutes)


if __name__ == "__main__":
    unittest.main()
