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

    profile_builder = ProfileBuilder(file_path, test_environment=False)
    fw_instructors, rw_instructors = profile_builder.build_instructor_profiles()

    available_fw_aircraft = {}
    available_rw_aircraft = {}
    aircraft_factory = AircraftFactory()
    calendar = Calendar(earliest_block=7, latest_block=17)
    earliest_block = calendar.earliest_block
    latest_block = calendar.latest_block

    available_rw_aircraft['R22'] = aircraft_factory.build_aircraft_of_model(
                                    name_prefix = 'R22',
                                    model = 'R22',
                                    num_aircraft = 6,
                                    earliest_block = earliest_block,
                                    latest_block = latest_block)

    available_rw_aircraft['R44'] = aircraft_factory.build_aircraft_of_model(
                                    name_prefix = 'R44',
                                    model = 'R44',
                                    num_aircraft = 3,
                                    earliest_block = earliest_block,
                                    latest_block = latest_block)

    available_rw_aircraft['RWSIM'] = aircraft_factory.build_aircraft_of_model(
                                    name_prefix = 'RWSIM',
                                    model = 'RWSIM',
                                    num_aircraft = 1,
                                    earliest_block = earliest_block,
                                    latest_block = latest_block,
                                    soloable=False)

    available_fw_aircraft['C172'] = aircraft_factory.build_aircraft_of_model(
                                    name_prefix = 'C172',
                                    model = 'C172',
                                    num_aircraft = 11,
                                    earliest_block = earliest_block,
                                    latest_block = latest_block)

    available_fw_aircraft['BARON'] = aircraft_factory.build_aircraft_of_model(
                                    name_prefix = 'BARON',
                                    model = 'BARON',
                                    num_aircraft = 1,
                                    earliest_block = earliest_block,
                                    latest_block = latest_block)

    available_fw_aircraft['FWSIM'] = aircraft_factory.build_aircraft_of_model(
                                    name_prefix = 'FWSIM',
                                    model = 'FWSIM',
                                    num_aircraft = 2,
                                    earliest_block = earliest_block,
                                    latest_block = latest_block,
                                    soloable=False)

    data = [('Fixed-Wing', fw_instructors, available_fw_aircraft), ('Rotor-Wing', rw_instructors, available_rw_aircraft)]

    for entry in data:
        title = entry[0]
        instructors = entry[1]
        available_aircraft = entry[2]
        result_set = set()

        print("\n======= {} Feasability =======".format(title))
        feasability_analyzer = Analyzer(instructors, calendar, available_aircraft)
        feasability_analyzer.check_for_sufficient_aircraft()
        print("--- Student Conflicts ---")
        feasability_analyzer.check_student_availability()

        print("\n\t----- Testing Individual Instructors -----")
        for instructor_name, instructor in instructors.items():
            test_instructors = {instructor_name : instructor}
            instructor_schedule_builder = ScheduleBuilder(test_instructors, calendar, available_aircraft, time_limit=60, test_environment=True)
            instructor_status, solution_log = instructor_schedule_builder.build_schedule()
            result_set.add(instructor_status)
            num_students = len(instructor.students)

            if instructor_status == 3 or instructor_status == 0:
                print("\tTesting: {}, result: {}".format(instructor_name, instructor_status))
                for i in range(num_students):
                    removed_student = instructor.students.pop(i)
                    removed_student_schedule_builder = ScheduleBuilder(test_instructors, calendar, available_aircraft, time_limit=20, test_environment=True)
                    removed_status, _ = removed_student_schedule_builder.build_schedule()
                    if removed_status == 2 or removed_status == 4:
                        print("\t\tRemoving {} resulted in {}".format(removed_student.full_name, removed_status))
                    instructor.students.insert(i, removed_student)

        # If all instructors are feasible, build the schedule
        if 3 not in result_set and 0 not in result_set:
            print("\n======= {} Schedule =======".format(title))
            schedule_builder = ScheduleBuilder(instructors, calendar, available_aircraft, time_limit=60*60*2)
            status, solution_log = schedule_builder.build_schedule()




    # print("\n======= FW Feasability =======")
    # feasability_analyzer = Analyzer(fw_instructors, calendar, available_fw_aircraft)
    # feasability_analyzer.check_for_sufficient_aircraft()
    # print("--- Student Conflicts ---")
    # feasability_analyzer.check_student_availability()

    # print("\n======= RW Feasability =======")
    # feasability_analyzer = Analyzer(rw_instructors, calendar, available_rw_aircraft)
    # feasability_analyzer.check_for_sufficient_aircraft()
    # print("--- Student Conflicts ---")
    # feasability_analyzer.check_student_availability()

    # print("\n======= FW Schedule =======")
    # schedule_builder = ScheduleBuilder(fw_instructors, calendar, available_fw_aircraft)
    # status, solution_log = schedule_builder.build_schedule()
    # print(status)


if __name__ == "__main__":
    main()
