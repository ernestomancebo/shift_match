import unittest

import pytest
from shift_match.models import Schedule
from shift_match.services import IOService, MatchingService, ParseService


class TestParseService(unittest.TestCase):

    def setUp(self):
        self.parse_service = ParseService()
        self.io_service = IOService()

    def test_schedule_valid_line(self):
        """A valid line is a key-value entry separated by an equals sign (=)"""

        valid_line = "Ernesto=something else"
        self.assertTrue(self.parse_service.is_schedule_valid(valid_line))

    def test_schedule_invalid_line(self):
        """A valid line is a key-value entry separated by an equals sign (=)"""

        valid_line = "Ernesto something else"
        self.assertFalse(self.parse_service.is_schedule_valid(valid_line))

    def test_is_shift_valid_valids(self):
        shifts = "MO10:00-12:00,TH12:00-14:00,SU20:00-21:00,SA14:00-18:00,SU20:00-21:00".split(
            ',')

        for s in shifts:
            self.assertTrue(self.parse_service.is_shift_valid(s))

    def test_is_shift_valid_invalids(self):
        shifts = "10:00-12:00,TH12-14:00,SU-21:00,:00-18:00,SU2021:00".split(
            ',')

        for s in shifts:
            self.assertFalse(self.parse_service.is_shift_valid(s))

    def test_parse_schedule_(self):
        lines = self.io_service.read_file('test/mock_data/example1.txt')
        self.assertEqual(3, len(lines))

        schedules = self.parse_service.parse_lines(lines)
        self.assertEqual(3, len(schedules))

        first_schedule: Schedule = schedules[0]
        self.assertEqual(5, len(first_schedule.schedule))

    def test_parse_schedule_invalid_line(self):
        with pytest.raises(AssertionError) as e:
            assert self.parse_service.parse_schedule("something that fails")
        assert e.value.args[0].startswith('Invalid line')

    def test_parse_schedule_invalid_shift(self):
        with pytest.raises(AssertionError) as e:
            self.parse_service.parse_schedule("RENE=MO10:15-ee:00")
        assert e.value.args[0].startswith('Invalid shift')

    def test_parse_schedule_invalid_time(self):
        with pytest.raises(AssertionError) as e:
            self.parse_service.parse_schedule("RENE=MO10:00-55:00")
        assert e.value.args[0].startswith('Unable to parse time')

    def test_parse_schedule_invalid_shif_time(self):
        with pytest.raises(AssertionError) as e:
            self.parse_service.parse_schedule("RENE=MO10:00-09:00")
        assert e.value.args[0].startswith('Shift time invalid')


class TestMatchingService(unittest.TestCase):

    def setUp(self):
        self.io_service = IOService()
        self.parse_service = ParseService()
        self.matching_service = MatchingService(self.io_service)

    def test_process_schedules_file1(self):
        lines = self.io_service.read_file('test/mock_data/example1.txt')
        schedules = self.parse_service.parse_lines(lines)
        matches = self.matching_service.process_schedules(schedules)

        self.assertEqual(
            3, len(matches), "There're three employees combinations that matches")
        match_1 = [2, 2, 3]
        for idx, match in enumerate(matches):
            self.assertEqual(match_1[idx], match[1])

        lines = self.io_service.read_file('test/mock_data/example2.txt')
        schedules = self.parse_service.parse_lines(lines)
        matches = self.matching_service.process_schedules(schedules)
        match_2 = [3]
        for idx, match in enumerate(matches):
            self.assertEqual(match_2[idx], match[1])

    def test_find_match_file2(self):
        lines = self.io_service.read_file('test/mock_data/example2.txt')
        self.assertEqual(2, len(lines))

        schedules = self.parse_service.parse_lines(lines)
        self.assertEqual(2, len(schedules))

        first_schedule: Schedule = schedules[0]
        self.assertEqual(5, len(first_schedule.schedule))

        matches = self.matching_service.find_matches(
            schedules[0], schedules[1])
        # These two schedules matches three times
        self.assertEqual(3, matches)


class TestIOService(unittest.TestCase):

    def setUp(self):
        self.io_service = IOService()

    def test_format_names(self):
        expected = '    thisis - a test    '
        self.assertEqual(
            expected, self.io_service.format_names("thisis", "a test"))

    def test_read_file(self):
        lines = self.io_service.read_file('test/mock_data/example1.txt')
        self.assertEqual(3, len(lines))

    def test_read_file_unexistent(self):
        with pytest.raises(FileNotFoundError) as e:
            assert self.io_service.read_file('test/mock_data/example1.xyz')
        self.assertEqual(
            "File test/mock_data/example1.xyz doesn't exists", e.value.args[0])
