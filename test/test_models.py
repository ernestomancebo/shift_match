import unittest
from datetime import datetime, timedelta

from shift_match.models import Shift
import copy

class TestModels(unittest.TestCase):

    def setUp(self):
        clock_in = datetime.today()
        clock_out = datetime.today()

        # Add 15 minutes
        clock_out = clock_out + timedelta(minutes=15)

        self.shift_under_test = Shift(clock_in.time(), clock_out.time())

    def test_shift_invalid(self):
        other_shift = copy.copy(self.shift_under_test)

        # Clock in time rebases the clock out
        other_shift.clock_in = (
            datetime.today() + timedelta(minutes=30)).time()
        self.assertFalse(other_shift.is_valid())

    def test_shift_valid(self):
        self.assertTrue(self.shift_under_test.is_valid())
