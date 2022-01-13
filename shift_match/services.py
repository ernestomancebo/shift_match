"""Wraps functionalities into services"""

import re
from datetime import datetime
from os import path

from shift_match.models import Schedule, Shift


class IOService():
    """Input and Output related functions"""

    def read_file(self, file_path):
        """Reads a file specified at [file_path]"""
        if not path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} doesn't exists")

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
        return lines

    def format_names(self, name_a, name_b):
        """Format the employees name that will be printed"""
        return '{0:>10} - {1:<10}'.format(name_a, name_b)

    def print_matches(self, matches_list: list):
        """Prints the matching schedules"""
        if len(matches_list) == 0:
            print('No matches found.')
            return

        # Header and its separating line
        header = '{0:^23} | {1}'.format('Employees', 'Times Matched')
        print(header)
        print('-' * len(header))

        for match in matches_list:
            print('{0} | {1}'.format(match[0], match[1]))


class ParseService():
    """Packs functionalities related from text to schedule and shift parsing"""

    def __init__(self):
        self.shift_regex = re.compile(
            r"(MO|TU|WE|TH|FR|SA|SU)(\d{1,2}:\d{2}-?){2}")
        self.time_format = "%H:%M"

    def parse_lines(self, lines: list):
        """Transform string lines into a list of Schedules"""

        schedules = []
        for line in lines:
            schedules.append(self.parse_schedule(line))

        return schedules

    def parse_schedule(self, line: str):
        """Build a Schedule object given a str (line)"""

        if not self.is_schedule_valid(line):
            raise AssertionError("Invalid line " + line)

        employee, shifts = line.split("=")

        schedule = {}
        for shift in shifts.split(','):
            if not self.is_shift_valid(shift):
                raise AssertionError("Invalid shift " + shift)

            day = shift[:2]
            clock_in, clock_out = shift.split("-")
            clock_in = clock_in[2:]

            try:
                clock_in = datetime.strptime(clock_in, self.time_format)
                clock_out = datetime.strptime(clock_out, self.time_format)
            except:
                raise AssertionError(
                    f"Unable to parse time. clock_in: {clock_in} ; clock_out: {clock_out}")

            shift_obj = Shift(clock_in.time(), clock_out.time())
            if not shift_obj.is_valid():
                raise AssertionError(f"Shift time invalid " + str(shift_obj))

            schedule[day] = shift_obj
        return Schedule(employee, schedule)

    def is_schedule_valid(self, line: str):
        """Ensures that the given string contains exactly one equals (=)"""
        return line.count("=") == 1

    def is_shift_valid(self, shift: str):
        """Returns True if the given [shift] matches the patter *DDHH:MM-HH:MM*"""
        return self.shift_regex.match(shift) is not None


class MatchingService():
    """Operations that identifies matching Shifts"""

    def __init__(self, io_service: IOService):
        self.io_service = io_service

    def process_schedules(self, schedules: list):
        """Given a Schedule list, counts how many times the employees matches"""

        schedules_length = len(schedules)
        matches_list = []

        for idx in range(0, schedules_length - 1):
            for next_idx in range(idx + 1, schedules_length):
                matches_count = self.find_matches(
                    schedules[idx], schedules[next_idx])

                if matches_count > 0:
                    stats = (self.io_service.format_names(
                        schedules[idx].employee, schedules[next_idx].employee), matches_count)
                    matches_list.append(stats)

        return matches_list

    def find_matches(self, schedule_a: Schedule, schedule_b: Schedule):
        """Look for matches given two schedules"""
        matches = 0
        for day in schedule_a.schedule.keys():
            # If matches the given day, look up
            # to see if matches also at the shift
            if schedule_b.schedule.get(day, False):
                matches += 1 if self.is_match(schedule_a.schedule.get(
                    day), schedule_b.schedule.get(day)) else 0
        return matches

    def is_match(self, shift_a: Shift, shift_b: Shift):
        """Given two shifts, if one of them clocks in
        within the other shift period, then it's a match."""

        a_clocked_first = shift_a.clock_in <= shift_b.clock_in
        if a_clocked_first:
            matched = shift_a.clock_in <= shift_b.clock_in < shift_a.clock_out
        else:
            matched = shift_b.clock_in <= shift_a.clock_in < shift_b.clock_out

        return matched
