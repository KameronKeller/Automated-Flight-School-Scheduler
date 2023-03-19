# from models.csv_parser import CsvParser
from models.person import Person
from models.profile_builder import ProfileBuilder
from models.schedule_builder import ScheduleBuilder
from models.calendar import Calendar
from models.aircraft_factory import AircraftFactory
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
    # pp.pprint(instructors['Stephen Shoffner'].unavailability)
    unavailability = {'fixedwing_friday_unavailability': '05:30;06:30;',
    'fixedwing_monday_unavailability': '06:30;05:30;09:30;11:30;10:30;',
    'fixedwing_saturday_unavailability': '05:30;06:30;07:30;08:30;09:30;10:30;11:30;12:30;13:30;14:30;15:30;16:30;17:30;18:30;19:30;20:30;',
    'fixedwing_sunday_unavailability': '05:30;06:30;07:30;08:30;09:30;10:30;11:30;12:30;13:30;14:30;15:30;16:30;17:30;18:30;19:30;20:30;',
    'fixedwing_thursday_unavailability': '05:30;06:30;',
    'fixedwing_tuesday_unavailability': '06:30;05:30;',
    'fixedwing_wednesday_unavailability': '05:30;06:30;'}
    person = Person('first', 'last', unavailability)
    pp.pprint(person.unavailability)

    # pp.pprint(instructors)
    # for student in instructors['Jason Axt'].students:
        # print(student.full_name)

if __name__ == "__main__":
    main()
