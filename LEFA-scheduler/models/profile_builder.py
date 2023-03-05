import csv

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
		for profile in profiles:
			if profile['instructor'] == "I am an instructor":
				print(profile['first_name'])

		# return instructors

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
					# may not need this, but adding just-in-case
					'submission_id' : row['ID'],
					'first_name' : row['What is your first name?'],
					'last_name' : row['What is your last name?'],
					'phone_number' : row['What is your phone number?'],
					'cocc_student' : row['Are you a COCC student?'],
					'instructor' : row['Who is your instructor?'],
					'current_rating' : row['What rating will you primarily be working on during the Winter term (January - April)?'],
					'schedule_type' : row['Are you scheduling Rotor-Wing or Fixed-Wing aircraft?'],
					'rotorwing_sunday_unavailability' : row['Sunday - Unavailability'],
					'rotorwing_monday_unavailability' : row['Monday - Unavailability'],
					'rotorwing_tuesday_unavailability' : row['Tuesday - Unavailability'],
					'rotorwing_wednesday_unavailability' : row['Wednesday - Unavailability'],
					'rotorwing_thursday_unavailability' : row['Thursday - Unavailability'],
					'rotorwing_friday_unavailability' : row['Friday - Unavailability'],
					'rotorwing_saturday_unavailability' : row['Saturday - Unavailability'],
					'rotorwing_time_off_explaination' : row['Explanation of Time Off'],
					'fixedwing_sunday_unavailability' : row['Sunday - Unavailability2'],
					'fixedwing_monday_unavailability' : row['Monday - Unavailability2'],
					'fixedwing_tuesday_unavailability' : row['Tuesday - Unavailability2'],
					'fixedwing_wednesday_unavailability' : row['Wednesday - Unavailability2'],
					'fixedwing_thursday_unavailability' : row['Thursday - Unavailability2'],
					'fixedwing_friday_unavailability' : row['Friday - Unavailability2'],
					'fixedwing_saturday_unavailability' : row['Saturday - Unavailability2'],
					'fixedwing_time_off_explaination' : row['Explanation of Time Off2']
				}
				profiles.append(profile)
		return profiles

	def verify_fieldnames(self, fieldnames):
		for required_fieldname in self.required_fieldnames:
			if required_fieldname not in fieldnames:
				print("ERROR: {} not found".format(required_fieldname))


