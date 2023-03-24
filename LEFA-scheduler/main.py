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
    # earliest_block = 0
    # latest_block = 24
    available_rw_aircraft['R22'] = aircraft_factory.build_aircraft_of_model(
                                    name_prefix = 'R22',
                                    model = 'R22',
                                    # num_aircraft = 10,
                                    num_aircraft = 6,
                                    earliest_block = earliest_block,
                                    latest_block = latest_block)

    available_rw_aircraft['R44'] = aircraft_factory.build_aircraft_of_model(
                                    name_prefix = 'R44',
                                    model = 'R44',
                                    # num_aircraft = 6,
                                    num_aircraft = 3,
                                    earliest_block = earliest_block,
                                    latest_block = latest_block)

    available_rw_aircraft['RWSIM'] = aircraft_factory.build_aircraft_of_model(
                                    name_prefix = 'RWSIM',
                                    model = 'RWSIM',
                                    # num_aircraft = 3,
                                    num_aircraft = 1,
                                    earliest_block = earliest_block,
                                    latest_block = latest_block,
                                    soloable=False)

    available_fw_aircraft['C172'] = aircraft_factory.build_aircraft_of_model(
                                    name_prefix = 'C172',
                                    model = 'C172',
                                    # num_aircraft = 15,
                                    num_aircraft = 11,
                                    earliest_block = earliest_block,
                                    latest_block = latest_block)

    available_fw_aircraft['BARON'] = aircraft_factory.build_aircraft_of_model(
                                    name_prefix = 'BARON',
                                    model = 'BARON',
                                    # num_aircraft = 3,
                                    num_aircraft = 1,
                                    earliest_block = earliest_block,
                                    latest_block = latest_block)

    available_fw_aircraft['FWSIM'] = aircraft_factory.build_aircraft_of_model(
                                    name_prefix = 'FWSIM',
                                    model = 'FWSIM',
                                    # num_aircraft = 3,
                                    num_aircraft = 2,
                                    earliest_block = earliest_block,
                                    latest_block = latest_block,
                                    soloable=False)
    print("\n======= FW Feasability =======")
    feasability_analyzer = Analyzer(fw_instructors, calendar, available_fw_aircraft)
    feasability_analyzer.check_for_sufficient_aircraft()
    print("--- Student Conflicts ---")
    feasability_analyzer.check_student_availability()

    print("\n======= RW Feasability =======")
    feasability_analyzer = Analyzer(rw_instructors, calendar, available_rw_aircraft)
    feasability_analyzer.check_for_sufficient_aircraft()
    print("--- Student Conflicts ---")
    feasability_analyzer.check_student_availability()

    print("\n======= RW Schedule =======")
    schedule_builder = ScheduleBuilder(rw_instructors, calendar, available_rw_aircraft)
    status, solution_log = schedule_builder.build_schedule()
    print(status)
    if status == 3:
        print("\t----- Testing Individual Instructors -----")
        for instructor_name, instructor in rw_instructors.items():
            test_instructors = {instructor_name : instructor}
            instructor_schedule_builder = ScheduleBuilder(test_instructors, calendar, available_rw_aircraft, time_limit=60, test_environment=True)
            instructor_status, solution_log = instructor_schedule_builder.build_schedule()
            # for student in instructor.students:
            #     print(student.full_name)
            if instructor_status == 3:
                print("\tTesting: {}, result: {}".format(instructor_name, instructor_status))
            #     print("test_this_one")

    print("\n======= FW Schedule =======")
    schedule_builder = ScheduleBuilder(fw_instructors, calendar, available_fw_aircraft, time_limit=60*60*2)
    status, solution_log = schedule_builder.build_schedule()
    print(status)
    if status == 3 or status == 0:
        print("\t----- Testing Individual Instructors -----")
        for instructor_name, instructor in fw_instructors.items():
            test_instructors = {instructor_name : instructor}
            instructor_schedule_builder = ScheduleBuilder(test_instructors, calendar, available_fw_aircraft, time_limit=60, test_environment=True)
            instructor_status, solution_log = instructor_schedule_builder.build_schedule()
            num_students = len(instructor.students)
            if instructor_status == 3 or instructor_status == 0:
                print("\tTesting: {}, result: {}".format(instructor_name, instructor_status))
                for i in range(num_students):
                    removed_student = instructor.students.pop(i)
                    removed_student_schedule_builder = ScheduleBuilder(test_instructors, calendar, available_fw_aircraft, time_limit=20, test_environment=True)
                    removed_status, _ = removed_student_schedule_builder.build_schedule()
                    if removed_status == 2 or removed_status == 4:
                        print("\t\tRemoving {} resulted in {}".format(removed_student.full_name, removed_status))
                    instructor.students.insert(i, removed_student)
                #     print(student.full_name)
            #     print("test_this_one")




                # original_students = copy.deepcopy(instructor.students)
                # for i in range(len(original_students)):
                #     students = copy.deepcopy(original_students)
                #     print('len(original_students)')
                #     print(len(original_students))
                #     removed_student = students.pop(i)
                #     instructor.students = students
                #     schedule_builder = ScheduleBuilder(test_instructors, calendar, available_rw_aircraft, test_environment=True)
                #     status, solution_log = schedule_builder.build_schedule()

                #     print("\t\tRemoved: {}, result: {}".format(removed_student.full_name, status))
            # print(instructor.students)

    # print("\n======= FW Schedule =======")
    # schedule_builder = ScheduleBuilder(fw_instructors, calendar, available_fw_aircraft)
    # status, solution_log = schedule_builder.build_schedule()
    # print(status)


if __name__ == "__main__":
    main()
