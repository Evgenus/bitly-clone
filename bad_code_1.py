import re
from datetime import datetime


ABBREVIATIONS_LINE_FORMAT = re.compile(r'^(\w+)_([a-zA-Z\s]+)_([a-zA-Z\s]+)$')


def create_racer_abbreviations(filename):
    """Retrieves {'abbreviation': (name, team)}" format dict from abbreviations.txt"""
    abbreviations = {}
    with open(filename, 'r') as fn:
        for line in fn:
            match_obj = ABBREVIATIONS_LINE_FORMAT.match(line)
            abbr, name, team = match_obj.groups()
            abbreviations[abbr] = (name,  team.rstrip())

    return abbreviations


TIMING_LINE_FORMAT = re.compile(r'^([A-Z]+).*(\d{2}:\d+:\d+\.\d+)$')


def retrieve_timings_from_log(filename):
    """returns timing log from start.log or end.log in {'abbreviation': time} format"""
    timing_log = {}
    with open(filename, 'r') as fn:
        for line in fn:
            # matches 2 groups: abbreviation of a racer and time
            match_obj = TIMING_LINE_FORMAT.match(line)
            key, raw_time = match_obj.groups()
            # converts time from a string to datetime object
            lap_time = datetime.strptime(raw_time.rstrip(), '%H:%M:%S.%f')
            # adds key, value to a timing_log
            timing_log[key] = lap_time

    return timing_log


def sorted_individual_results(start_timings, end_timings, reverse_order=False):
    """
    Receives start and end timings and returns an OrderedDict with
    {abbreviations:timedeltas}
    """
    # creating dict with best lap results
    lap_results = {
        key: end_timings[key] - start_timings[key]
        for key, value in start_timings.items()
    }
    sorted_results = dict(sorted(
        lap_results.items(),
        key=lambda x: x[1],
        reverse=reverse_order,
    ))
    return sorted_results


def print_result_board(sorted_lap_results, abbreviations):
    """prints result board to a console"""
    for counter, (key, value) in enumerate(sorted_lap_results.items(), start=1):
        racer_name, team_name = abbreviations[key]
        best_time = str(value)[2:-3]
        counter_str = str(counter) + '.'
        print(f"{counter_str: <3} {racer_name: <18} | {team_name: <30}  | {best_time}")
        if counter == 15:
            print('-' * 70)


def main():
    start_timings = retrieve_timings_from_log('start.log')
    end_timings = retrieve_timings_from_log('end.log')
    # {'abbreviation of pilot': ('name of pilot, 'team')}
    abbreviations = create_racer_abbreviations('abbreviations.txt')
    sorted_lap_results = sorted_individual_results(start_timings, end_timings)
    print_result_board(sorted_lap_results, abbreviations)


if __name__ == '__main__':
    main()
