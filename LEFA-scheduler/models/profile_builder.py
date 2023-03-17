import csv
from models.instructor import Instructor
from models.student import Student
from models.instructor_student import InstructorStudent

class ProfileBuilder:

	def __init__(self, csv_path):
		self.csv_path = csv_path
		self.required_fieldnames = {
			'ID',
			'What is your first name?',
			'What is your last name?',
			'What is your phone number?',
			'Are you a COCC student?',
			'Who is your instructor?',
			'What rating will you primarily be working on during the Winter term (January - April)?',
			'Are you scheduling Rotor-Wing or Fixed-Wing aircraft?',
			'Sunday - Unavailability',
			'Monday - Unavailability',
			'Tuesday - Unavailability',
			'Wednesday - Unavailability',
			'Thursday - Unavailability',
			'Friday - Unavailability',
			'Saturday - Unavailability',
			'Explanation of Time Off',
			'Sunday - Unavailability2',
			'Monday - Unavailability2',
			'Tuesday - Unavailability2',
			'Wednesday - Unavailability2',
			'Thursday - Unavailability2',
			'Friday - Unavailability2',
			'Saturday - Unavailability2',
			'Explanation of Time Off2'
		}

	def build_instructor_profiles(self):
		profiles = self.create_profiles()
		instructors = {}
		students = set()
		for profile in profiles:
			full_name = profile['full_name']
			if profile['instructor'] == "I am an instructor":
				# unavailability = get_unavailability(profile)
				if profile['schedule_type'] == 'Rotor-Wing':
					unavailability = profile['rotorwing_unavailability']
				else:
					unavailability = profile['fixedwing_unavailability']

				instructors[full_name] = Instructor(profile['first_name'], profile['last_name'], unavailability)
			else:
				students.add(profile['full_name'])

		for profile in profiles:
			instructor_name = profile['instructor']
			if profile['instructor'] in instructors:
				if profile['schedule_type'] == 'Rotor-Wing':
					unavailability = profile['rotorwing_unavailability']
				else:
					unavailability = profile['fixedwing_unavailability']

				if profile['full_name'] in instructors and profile['full_name'] in students:
					# print('found the instructorStudents {}'.format(profile['full_name']))
					instructor_student = InstructorStudent(profile['first_name'], profile['last_name'], unavailability, profile['current_rating'], instructors[instructor_name], instructors[profile['full_name']].students)
					instructors[instructor_name].add_student(instructor_student)
					instructors[profile['full_name']] = instructor_student
				else:
					student = Student(profile['first_name'], profile['last_name'], unavailability, profile['current_rating'], instructors[instructor_name])
					instructors[instructor_name].add_student(student)
			else:
				if instructor_name != "I am an instructor":
					print("instructor not found!!!! {}".format(instructor_name))

		return instructors

	def create_profiles(self):
		profiles = []

		# Note: encoding is required to handle special characters.
		# https://stackoverflow.com/questions/19699367/for-line-in-results-in-unicodedecodeerror-utf-8-codec-cant-decode-byte
		with open(self.csv_path, encoding = "ISO-8859-1") as csv_file:
			csv_reader = csv.DictReader(csv_file)
			# headers = next(csv_reader)

			self.verify_fieldnames(csv_reader.fieldnames)

			for row in csv_reader:
				# print(row)

				profile = {
					# may not need submission_id, but adding just-in-case
					'submission_id' : row['ID'],
					'first_name' : row['What is your first name?'],
					'last_name' : row['What is your last name?'],
					'full_name' : row['What is your first name?'] + ' ' + row['What is your last name?'],
					'phone_number' : row['What is your phone number?'],
					'cocc_student' : row['Are you a COCC student?'],
					'instructor' : row['Who is your instructor?'],
					'current_rating' : row['What rating will you primarily be working on during the Winter term (January - April)?'],
					'schedule_type' : row['Are you scheduling Rotor-Wing or Fixed-Wing aircraft?'],
					'rotorwing_unavailability' : {
						'rotorwing_sunday_unavailability' : row['Sunday - Unavailability'],
						'rotorwing_monday_unavailability' : row['Monday - Unavailability'],
						'rotorwing_tuesday_unavailability' : row['Tuesday - Unavailability'],
						'rotorwing_wednesday_unavailability' : row['Wednesday - Unavailability'],
						'rotorwing_thursday_unavailability' : row['Thursday - Unavailability'],
						'rotorwing_friday_unavailability' : row['Friday - Unavailability'],
						'rotorwing_saturday_unavailability' : row['Saturday - Unavailability'],
						'rotorwing_time_off_explaination' : row['Explanation of Time Off'],
					},
					'fixedwing_unavailability' : {
						'fixedwing_sunday_unavailability' : row['Sunday - Unavailability2'],
						'fixedwing_monday_unavailability' : row['Monday - Unavailability2'],
						'fixedwing_tuesday_unavailability' : row['Tuesday - Unavailability2'],
						'fixedwing_wednesday_unavailability' : row['Wednesday - Unavailability2'],
						'fixedwing_thursday_unavailability' : row['Thursday - Unavailability2'],
						'fixedwing_friday_unavailability' : row['Friday - Unavailability2'],
						'fixedwing_saturday_unavailability' : row['Saturday - Unavailability2'],
						'fixedwing_time_off_explaination' : row['Explanation of Time Off2']
					}
				}
				profiles.append(profile)
		return profiles

	def verify_fieldnames(self, fieldnames):
		for required_fieldname in self.required_fieldnames:
			if required_fieldname not in fieldnames:
				raise KeyError('CSV file must contain required fieldnames')



