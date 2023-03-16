import unittest
from models.profile_builder import ProfileBuilder
from models.student import Student

fake_csv_path_large = 'tests/fake_data.csv'
fake_csv_path_simple = 'tests/fake_data_simple.csv'
required_fieldnames = {
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

class TestProfileBuilder(unittest.TestCase):

	def setUp(self):
		self.profile_builder = ProfileBuilder(fake_csv_path_simple)

	def test_attributes(self):
		self.assertEqual(fake_csv_path_simple, self.profile_builder.csv_path)
		self.assertEqual(required_fieldnames, self.profile_builder.required_fieldnames)

	def test_create_profiles(self):
		profiles = self.profile_builder.create_profiles()
		self.assertEqual(len(profiles), 8)
		test_profile = profiles[0]
		self.assertEqual(test_profile['submission_id'], '1906')
		self.assertEqual(test_profile['first_name'], 'Porter')
		self.assertEqual(test_profile['last_name'], 'Darleen')
		self.assertEqual(test_profile['phone_number'], '7839159761')
		self.assertEqual(test_profile['cocc_student'], 'Yes')
		self.assertEqual(test_profile['instructor'], 'Garth Conrad')
		self.assertEqual(test_profile['current_rating'], 'CFI')
		self.assertEqual(test_profile['schedule_type'], 'Rotor-Wing')
		self.assertEqual(test_profile['rotorwing_unavailability']['rotorwing_sunday_unavailability'],
			'05:00;06:00;07:00;08:00;14:00;13:00;12:00;11:00;10:00;09:00;')
		self.assertEqual(test_profile['fixedwing_unavailability']['fixedwing_sunday_unavailability'], '')

	def test_build_instructor_profiles(self):
		instructors = self.profile_builder.build_instructor_profiles()
		instructor = instructors['Garth Conrad']
		self.assertEqual(len(instructors), 1)
		self.assertEqual(instructor.full_name, 'Garth Conrad')
		self.assertEqual(len(instructor.students), 7)
		student = instructor.students[0]
		self.assertIsInstance(student, Student)

	def test_verify_fieldnames(self):
		fieldnames = ['ID', 'Start time', 'Completion time', 'Email', 'Name', 'What is your first name?', 'What is your last name?', 'What is your phone number?', 'Are you a COCC student?', 'Who is your instructor?', 'What rating will you primarily be working on during the Winter term (January - April)?', 'Are you scheduling Rotor-Wing or Fixed-Wing aircraft?', 'Sunday - Unavailability', 'Monday - Unavailability', 'Tuesday - Unavailability', 'Wednesday - Unavailability', 'Thursday - Unavailability', 'Friday - Unavailability', 'Saturday - Unavailability', 'Explanation of Time Off', 'Sunday - Unavailability2', 'Monday - Unavailability2', 'Tuesday - Unavailability2', 'Wednesday - Unavailability2', 'Thursday - Unavailability2', 'Friday - Unavailability2', 'Saturday - Unavailability2', 'Explanation of Time Off2', 'FULL NAME']
		try:
			self.profile_builder.verify_fieldnames(fieldnames)
		except KeyError:
			self.fail("verify_fieldnames raised KeyError unexpectedly!")

	def test_verify_fieldnames_throws_error(self):
		fieldnames = ['test']
		with self.assertRaises(KeyError):
			self.profile_builder.verify_fieldnames(fieldnames)


if __name__ == '__main__':
    unittest.main()
