"""Application models"""

import datetime


class Schedule():
    """Schedule for a employee"""

    def __init__(self, employee, schedule: dict):
        self.employee = employee
        self.schedule = schedule

    def __str__(self):
        """String representation of a Schedule object"""
        return f"<Schedule for employee: {self.employee} >"


class Shift():
    """Object that represents the time an employee clocks in and out"""

    def __init__(self, clock_in: datetime.time, clock_out: datetime.time):
        self.clock_in = clock_in
        self.clock_out = clock_out

    def is_valid(self):
        """Returns True if the clock_in is before clock_out, False otherwise"""
        return (self.clock_in and self.clock_out) and (self.clock_in < self.clock_out)

    def __str__(self):
        """String representation of a Shift object"""
        return f"<Shift clock_in: {self.clock_in} ; clock_out: {self.clock_out} >"
