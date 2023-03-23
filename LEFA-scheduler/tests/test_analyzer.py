import unittest
from models.analyzer import Analyzer
from models.instructor import Instructor
from models.calendar import Calendar
from models.aircraft_factory import AircraftFactory
from tests.factory.instructor_factory import InstructorFactory
from tests.factory.student_factory import StudentFactory

class TestAnalyzer(unittest.TestCase):

	def setUp(self):
		self.available_aircraft = {}
		self.calendar = Calendar(earliest_block=7, latest_block=17)
		aircraft_factory = AircraftFactory()
		earliest_block = self.calendar.earliest_block
		latest_block = self.calendar.latest_block

		self.available_aircraft['R22'] = aircraft_factory.build_aircraft_of_model(
										name_prefix = 'R22',
										model = 'R22',
										num_aircraft = 6,
										earliest_block = earliest_block,
										latest_block = latest_block)

		self.available_aircraft['R44'] = aircraft_factory.build_aircraft_of_model(
										name_prefix = 'R44',
										model = 'R44',
										num_aircraft = 3,
										earliest_block = earliest_block,
										latest_block = latest_block)

		self.available_aircraft['RWSIM'] = aircraft_factory.build_aircraft_of_model(
										name_prefix = 'RWSIM',
										model = 'RWSIM',
										num_aircraft = 1,
										earliest_block = earliest_block,
										latest_block = latest_block,
										soloable=False)

		self.available_aircraft['C172'] = aircraft_factory.build_aircraft_of_model(
										name_prefix = 'C172',
										model = 'C172',
										num_aircraft = 11,
										earliest_block = earliest_block,
										latest_block = latest_block)

		self.available_aircraft['BARON'] = aircraft_factory.build_aircraft_of_model(
										name_prefix = 'BARON',
										model = 'BARON',
										num_aircraft = 1,
										earliest_block = earliest_block,
										latest_block = latest_block)

		self.available_aircraft['FWSIM'] = aircraft_factory.build_aircraft_of_model(
										name_prefix = 'FWSIM',
										model = 'FWSIM',
										num_aircraft = 1,
										earliest_block = earliest_block,
										latest_block = latest_block,
										soloable=False)

		self.calendar = Calendar(earliest_block=7, latest_block=17)
		self.instructors = {}
		self.instructor = InstructorFactory.create_free_instructor()
		self.s1 = StudentFactory.create_free_student(first_name='s1', rating='Commercial', schedule_type='Fixed-Wing')
		self.s2 = StudentFactory.create_student(first_name='s2', rating='Instrument', schedule_type='Rotor-Wing')
		self.s3 = StudentFactory.create_one_block_student(first_name='s3', last_name='')
		self.instructor.add_student(self.s1)
		self.instructor.add_student(self.s2)
		self.instructor.add_student(self.s3)
		self.instructors[self.instructor.full_name] = self.instructor
		self.analyzer = Analyzer(self.instructors, self.calendar, self.available_aircraft)

	# def test_calculates_num_aircraft_needed(self):
	# 	self.analyzer.check_for_sufficient_aircraft()

	# def test_if_students_have_enough_availability_self(self):
	# 	self.analyzer.check_student_availability()


if __name__ == '__main__':
	unittest.main()
