# from models.csv_parser import CsvParser
# from models.person import Person
from models.profile_builder import ProfileBuilder
from models.schedule_builder import ScheduleBuilder
from models.calendar import Calendar
from models.aircraft_factory import AircraftFactory
from models.analyzer import Analyzer
import csv
import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)

def main():
    if len(sys.argv) != 2:
        print("usage: main.py input_csv")
        sys.exit(0)

    file_path = sys.argv[1]

    profile_builder = ProfileBuilder(file_path)
    instructors = profile_builder.build_instructor_profiles()

    available_aircraft = {}
    aircraft_factory = AircraftFactory()
    calendar = Calendar(earliest_block=7, latest_block=17)
    earliest_block = calendar.earliest_block
    latest_block = calendar.latest_block
    # earliest_block = 0
    # latest_block = 24
    available_aircraft['R22'] = aircraft_factory.build_aircraft_of_model(
                                    name_prefix = 'R22',
                                    model = 'R22',
                                    # num_aircraft = 10,
                                    num_aircraft = 6,
                                    earliest_block = earliest_block,
                                    latest_block = latest_block)

    available_aircraft['R44'] = aircraft_factory.build_aircraft_of_model(
                                    name_prefix = 'R44',
                                    model = 'R44',
                                    # num_aircraft = 6,
                                    num_aircraft = 3,
                                    earliest_block = earliest_block,
                                    latest_block = latest_block)

    available_aircraft['RWSIM'] = aircraft_factory.build_aircraft_of_model(
                                    name_prefix = 'RWSIM',
                                    model = 'RWSIM',
                                    # num_aircraft = 3,
                                    num_aircraft = 1,
                                    earliest_block = earliest_block,
                                    latest_block = latest_block,
                                    soloable=False)

    available_aircraft['C172'] = aircraft_factory.build_aircraft_of_model(
                                    name_prefix = 'C172',
                                    model = 'C172',
                                    # num_aircraft = 15,
                                    num_aircraft = 11,
                                    earliest_block = earliest_block,
                                    latest_block = latest_block)

    available_aircraft['BARON'] = aircraft_factory.build_aircraft_of_model(
                                    name_prefix = 'BARON',
                                    model = 'BARON',
                                    # num_aircraft = 3,
                                    num_aircraft = 1,
                                    earliest_block = earliest_block,
                                    latest_block = latest_block)

    available_aircraft['FWSIM'] = aircraft_factory.build_aircraft_of_model(
                                    name_prefix = 'FWSIM',
                                    model = 'FWSIM',
                                    # num_aircraft = 3,
                                    num_aircraft = 1,
                                    earliest_block = earliest_block,
                                    latest_block = latest_block,
                                    soloable=False)

    feasability_analyzer = Analyzer(instructors, calendar, available_aircraft)
    feasability_analyzer.check_for_sufficient_aircraft()
    feasability_analyzer.check_student_availability()

    schedule_builder = ScheduleBuilder(instructors, calendar, available_aircraft)
    status, solution_log = schedule_builder.build_schedule()
    print(status)


if __name__ == "__main__":
    main()
