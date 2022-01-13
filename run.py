from sys import argv

from shift_match.services import IOService, MatchingService, ParseService


def process_file(file_path: str):
    io = IOService()
    parser = ParseService()
    matcher = MatchingService(io)

    # Read an load schedules
    lines = io.read_file(file_path)
    schedule_list = parser.parse_lines(lines)

    # Look up for matches and print em
    matches = matcher.process_schedules(schedule_list)
    io.print_matches(matches)


if __name__ == '__main__':
    file_path = argv[1]
    process_file(file_path)
