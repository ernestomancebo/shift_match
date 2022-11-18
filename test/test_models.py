import unittest
from datetime import datetime, timedelta

from shift_match.models import Shift
import copy

class TestModels(unittest.TestCase):

    def setUp(self):
        self.shift_under_test = self.__get_shift()

    def __get_shift(self) -> Shift:
        clock_in = datetime.today()
        clock_out = datetime.today()

        # Add 15 minutes
        clock_out = clock_out + timedelta(minutes=15)

        shift = Shift(clock_in.time(), clock_out.time())
        
        return shift


    def test_shift_invalid(self):
        other_shift = self.__get_shift()

        # Clock in time rebases the clock out
        other_shift.clock_in = (
            datetime.today() + timedelta(minutes=30)).time()
        self.assertFalse(other_shift.is_valid())

    def test_shift_valid(self):
        self.assertTrue(self.shift_under_test.is_valid())
