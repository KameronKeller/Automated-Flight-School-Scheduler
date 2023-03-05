# from models.csv_parser import CsvParser
# from models.person import Person
from models.profile_builder import ProfileBuilder
import csv
import sys

def main():
    if len(sys.argv) != 2:
        print("usage: main.py input_csv")
        sys.exit(0)

    file_path = sys.argv[1]

    profile_builder = ProfileBuilder(file_path)
    instructors = profile_builder.build_instructor_profiles()
    print(instructors)
    # schedule_builder = ScheduleBuilder(instructors, aircraft, days)
    # schedule_builder.generate_model()
    # schedule_builder.compute_restraints()
    # schedule_builder.output_schedule()



    # parse_csv()
    # generate_model()
    # build_constraints()
    # generate_schedule()





    # # csv = CsvParser("submissions_data.csv")
    # # csv.get_names()

    # people = []

    # with open('submissions_data.csv') as csv_file:
    #     # csv_reader = csv.DictReader(csv_file)
    #     csv_reader = csv.reader(csv_file)
    #     for row in csv_reader:
    #         unavailability = {
    #             # "sunday" : row['Sunday - Unavailability'],
    #             # "monday" : row['Monday - Unavailability'],
    #             # "tuesday" : row['Tuesday - Unavailability'],
    #             # "wednesday" : row['Wednesday - Unavailability'],
    #             # "thursday" : row['Thursday - Unavailability'],
    #             # "friday" : row['Friday - Unavailability'],
    #             # "saturday" : row['Saturday - Unavailability']
    #             "sunday" : row[12],
    #             "monday" : row[13],
    #             "tuesday" : row[14],
    #             "wednesday" : row[15],
    #             "thursday" : row[16],
    #             "friday" : row[17],
    #             "saturday" : row[18]

    #         }
    #         unavailability = CsvParser
    #         person = Person(row[5], row[6], unavailability)
    #         people.append(person)
    #     # print(people[0].parse_unavailability(people[1].unavailability))
    #     print(people[1].unavailability)
    #         # name = row['What is your first name?'] + row['What is your last name?']
    #         # if name in people:
    #         #     print("Skipping duplicate: {}".format(name))
    #         # else:
    #         #     people.append(person)


    #     # headers = csv_reader.fieldnames

    #     # print(headers)


if __name__ == "__main__":
    main()
