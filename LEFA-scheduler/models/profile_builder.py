import csv
import string
from difflib import SequenceMatcher
from models.instructor import Instructor
from models.student import Student
from models.instructor_student import InstructorStudent

class ProfileBuilder:

	def __init__(self, csv_path, test_environment=True):
		self.csv_path = csv_path
		self.test_environment = test_environment
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
		solo_flight_id = 0
		solo_instructor_unavailability = {
				'Sunday': '',
				'Monday': '',
				'Tuesday': '',
				'Wednesday': '',
				'Thursday': '',
				'Friday': '',
				'Saturday': ''}



		profiles = self.create_profiles()
		instructors = None
		fw_instructors = {}
		rw_instructors = {}
		students = set()
		for profile in profiles:
			full_name = profile['full_name']
			if profile['instructor'] == "I am an instructor":
				# unavailability = get_unavailability(profile)
				if profile['schedule_type'] == 'Rotor-Wing':
					unavailability = profile['rotorwing_unavailability']
					rw_instructors[full_name] = Instructor(profile['first_name'], profile['last_name'], unavailability)
				else:
					unavailability = profile['fixedwing_unavailability']
					fw_instructors[full_name] = Instructor(profile['first_name'], profile['last_name'], unavailability)

			else:
				students.add(profile['full_name']) # keep track of students for second pass

		for profile in profiles:
			profile_type = profile['schedule_type']
			if profile_type == 'Rotor-Wing':
				instructors = rw_instructors
			else:
				instructors = fw_instructors

			instructor_name = profile['instructor']
			if profile['instructor'] in instructors:
				if profile_type == 'Rotor-Wing':
					unavailability = profile['rotorwing_unavailability']
					instructors = rw_instructors
				else:
					unavailability = profile['fixedwing_unavailability']
					instructors = fw_instructors

				if profile['full_name'] in instructors and profile['full_name'] in students:
					instructor_student = InstructorStudent(profile['first_name'], profile['last_name'], unavailability, profile['current_rating'], profile_type, instructors[instructor_name], instructors[profile['full_name']].students)

					instructors[instructor_name].add_student(instructor_student)
					instructors[profile['full_name']] = instructor_student
				else:
					# create the students
					student = Student(profile['first_name'], profile['last_name'], unavailability, profile['current_rating'], profile_type, instructors[instructor_name])
					
					# if they need solo, add a 'solo instructor'
					for aircraft_model, flight_configuration in student.aircraft.items():
						if 'solo' in flight_configuration:
							solo_instructor = Instructor(first_name='SOLO FLIGHT', last_name=str(solo_flight_id), unavailability=solo_instructor_unavailability, solo_placeholder=True)
							solo_flight_id += 1
							solo_instructor.add_student(student)
							instructors[solo_instructor.full_name] = solo_instructor


					instructors[instructor_name].add_student(student)
			else:
				if instructor_name != "I am an instructor":
					name = profile['full_name']
					if name != ' ':
						print('{} needs an instructor'.format(name))

		return fw_instructors, rw_instructors

	def create_profiles(self):
		profiles = []
		people = {}
		# Note: encoding is required to handle special characters.
		# https://stackoverflow.com/questions/19699367/for-line-in-results-in-unicodedecodeerror-utf-8-codec-cant-decode-byte
		with open(self.csv_path, encoding = "ISO-8859-1") as csv_file:
			csv_reader = csv.DictReader(csv_file)
			# headers = next(csv_reader)

			self.verify_fieldnames(csv_reader.fieldnames)

			for row in csv_reader:
				# print(row)

				first_name = row['What is your first name?']
				last_name = row['What is your last name?']
				first_name = first_name.strip()
				last_name = last_name.strip()
				full_name = first_name + ' ' + last_name

				profile = {
					# may not need submission_id, but adding just-in-case
					'submission_id' : row['ID'],
					'first_name' : first_name,
					'last_name' : last_name,
					'full_name' : full_name,
					'phone_number' : row['What is your phone number?'],
					'cocc_student' : row['Are you a COCC student?'],
					'instructor' : row['Who is your instructor?'],
					'current_rating' : row['What rating will you primarily be working on during the Winter term (January - April)?'],
					'schedule_type' : row['Are you scheduling Rotor-Wing or Fixed-Wing aircraft?'],
					'rotorwing_unavailability' : {
						'Sunday' : row['Sunday - Unavailability'],
						'Monday' : row['Monday - Unavailability'],
						'Tuesday' : row['Tuesday - Unavailability'],
						'Wednesday' : row['Wednesday - Unavailability'],
						'Thursday' : row['Thursday - Unavailability'],
						'Friday' : row['Friday - Unavailability'],
						'Saturday' : row['Saturday - Unavailability'],
					},
					'rotorwing_time_off_explaination' : row['Explanation of Time Off'],
					'fixedwing_unavailability' : {
						'Sunday' : row['Sunday - Unavailability2'],
						'Monday' : row['Monday - Unavailability2'],
						'Tuesday' : row['Tuesday - Unavailability2'],
						'Wednesday' : row['Wednesday - Unavailability2'],
						'Thursday' : row['Thursday - Unavailability2'],
						'Friday' : row['Friday - Unavailability2'],
						'Saturday' : row['Saturday - Unavailability2'],
					},
						'fixedwing_time_off_explaination' : row['Explanation of Time Off2']
				}

				if not self.test_environment:
					name = profile['full_name']
					if name != ' ':
						instructor = profile['instructor']
						if name not in people:
							# Check similarity
							for existing_name in people.keys():
								similarity = self.similar(name, existing_name)
								if similarity >= 0.85:
									print('{} is very similar to {}, are they duplicates?'.format(name, existing_name))

							people[name] = [instructor]
						else:
							people[name].append(instructor)
							instructors = people[name]
							if len(set(instructors)) == 1:
								print('Duplicate found: {}, Instructors: {}'.format(name, people[name]))


				profiles.append(profile)
		return profiles

	def verify_fieldnames(self, fieldnames):
		for required_fieldname in self.required_fieldnames:
			if required_fieldname not in fieldnames:
				raise KeyError('CSV file must contain required fieldnames')

	def similar(self, a, b):
		return SequenceMatcher(None, a, b).ratio()

