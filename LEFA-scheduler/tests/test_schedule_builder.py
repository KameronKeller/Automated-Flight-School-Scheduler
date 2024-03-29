import unittest
from ortools.sat.python import cp_model
from models.schedule_builder import ScheduleBuilder
from models.instructor import Instructor
from models.profile_builder import ProfileBuilder
from models.instructor_student import InstructorStudent
from tests.factory.instructor_factory import InstructorFactory
from tests.factory.student_factory import StudentFactory
from tests.factory.unavailability_factory import UnavailabilityFactory
from tests.factory.instructor_student_factory import InstructorStudentFactory
from models.aircraft_factory import AircraftFactory
from models.student import Student
from models.calendar import Calendar
import pprint as pp
from collections import Counter

class TestScheduleBuilder(unittest.TestCase):

	def setUp(self):
		self.calendar = Calendar(earliest_block=7, latest_block=17)
		self.free_instructor = InstructorFactory.create_free_instructor()
		self.free_instructors = {self.free_instructor.full_name : self.free_instructor}

		self.one_block_instructor = InstructorFactory.create_one_block_instructor()
		self.one_block_instructors = {self.one_block_instructor.full_name : self.one_block_instructor}

		self.unavailable_instructor = InstructorFactory.create_unavailable_instructor()
		self.unavailable_instructors = {self.unavailable_instructor.full_name : self.unavailable_instructor}

		self.earliest_block = 7
		self.latest_block = 17

		self.available_aircraft = {}
		self.aircraft_factory = AircraftFactory()
		self.available_aircraft['R22'] = self.aircraft_factory.build_aircraft_of_model(
										name_prefix = 'R22',
										model = 'R22',
										num_aircraft = 1,
										earliest_block = self.earliest_block,
										latest_block = self.latest_block)

		self.many_aircraft = {}
		self.many_aircraft['R22'] = self.aircraft_factory.build_aircraft_of_model(
										name_prefix = 'R22',
										model = 'R22',
										num_aircraft = 1,
										earliest_block = self.earliest_block,
										latest_block = self.latest_block)

		self.many_aircraft['R44'] = self.aircraft_factory.build_aircraft_of_model(
										name_prefix = 'R44',
										model = 'R44',
										num_aircraft = 1,
										earliest_block = self.earliest_block,
										latest_block = self.latest_block)

		self.many_aircraft['RWSIM'] = self.aircraft_factory.build_aircraft_of_model(
										name_prefix = 'RWSIM',
										model = 'RWSIM',
										num_aircraft = 1,
										earliest_block = self.earliest_block,
										latest_block = self.latest_block,
										soloable=False)

		self.many_aircraft['C172'] = self.aircraft_factory.build_aircraft_of_model(
										name_prefix = 'C172',
										model = 'C172',
										num_aircraft = 1,
										earliest_block = self.earliest_block,
										latest_block = self.latest_block)

		self.many_aircraft['BARON'] = self.aircraft_factory.build_aircraft_of_model(
										name_prefix = 'BARON',
										model = 'BARON',
										num_aircraft = 1,
										earliest_block = self.earliest_block,
										latest_block = self.latest_block)

		self.many_aircraft['FWSIM'] = self.aircraft_factory.build_aircraft_of_model(
										name_prefix = 'FWSIM',
										model = 'FWSIM',
										num_aircraft = 1,
										earliest_block = self.earliest_block,
										latest_block = self.latest_block,
										soloable=False)

		# self.instructor = Instructor('first', 'last', 'unavailable')
	#     # self.aircraft = Aircraft()
	#     self.schedule_builder = ScheduleBuilder([self.instructor])

	# def test_attributes(self):
	#     self.assertEqual(self.schedule_builder.instructors, [self.instructor])

	def test_flights_not_scheduled_when_instructor_unavailable(self):
		student = StudentFactory.create_free_student()
		self.unavailable_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.unavailable_instructors, self.calendar, self.available_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		self.assertEqual(status, cp_model.INFEASIBLE)

	def test_flights_not_scheduled_when_student_unavailable(self):
		student = StudentFactory.create_free_student()
		self.unavailable_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.unavailable_instructors, self.calendar, self.available_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		self.assertEqual(status, cp_model.INFEASIBLE)

	def test_student_has_one_flight_per_day_max(self):
		student = StudentFactory.create_three_blocks_three_days_student(first_name='Student', last_name='L', rating='Private', schedule_type='Rotor-Wing', instructor=self.free_instructor.full_name)
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, self.calendar, self.available_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		self.assertTrue(len(solution_log['days']) == len(set(solution_log['days'])))
		self.assertEqual(status, cp_model.FEASIBLE)

	def test_student_with_solo_and_dual_flights_only_flies_once_per_day(self):
		available_aircraft_c172 = {}
		available_aircraft_c172['C172'] = self.aircraft_factory.build_aircraft_of_model(
							name_prefix = 'C172',
							model = 'C172',
							num_aircraft = 1,
							earliest_block = 7,
							latest_block = 17)
		available_aircraft_c172['FWSIM'] = self.aircraft_factory.build_aircraft_of_model(
							name_prefix = 'FWSIM',
							model = 'FWSIM',
							num_aircraft = 1,
							earliest_block = 7,
							latest_block = 17,
							soloable=False)

		student = StudentFactory.create_free_student(rating='Commercial', schedule_type='Fixed-Wing', instructor=self.free_instructor.full_name)

		instructors = {}

		primary_instructor = InstructorFactory.create_free_instructor()
		primary_instructor.full_name = "Primary Instructor"
		primary_instructor.add_student(student)
		instructors[primary_instructor.full_name] = primary_instructor

		solo_instructor_placeholder = InstructorFactory.create_free_instructor()
		solo_instructor_placeholder.full_name = "SOLO FLIGHT"
		solo_instructor_placeholder.solo_placeholder = True
		solo_instructor_placeholder.add_student(student)
		instructors[solo_instructor_placeholder.full_name] = solo_instructor_placeholder

		schedule_builder = ScheduleBuilder(instructors, self.calendar, available_aircraft_c172, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		self.assertTrue(len(solution_log['days']) == len(set(solution_log['days'])))
		self.assertEqual(status, cp_model.FEASIBLE)


	def test_student_has_only_one_free_block_results_in_infeasable(self):
		# student requires 3 flights
		student = StudentFactory.create_one_block_student(first_name='Student', last_name='L', rating='Private', schedule_type='Rotor-Wing', instructor=self.free_instructor.full_name)
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, self.calendar, self.available_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		self.assertEqual(status, cp_model.INFEASIBLE)

	def test_instructor_has_only_one_free_block_results_in_infeasable(self):
		# student requires 3 flights
		student = StudentFactory.create_free_student()
		self.one_block_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.one_block_instructors, self.calendar, self.available_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		self.assertEqual(status, cp_model.INFEASIBLE)

	# def test_instructor_has_one_student_at_a_given_time(self):
	# 	available_aircraft_2 = {}
	# 	available_aircraft_2['R22'] = self.aircraft_factory.build_aircraft_of_model(
	# 						name_prefix = 'R22',
	# 						model = 'R22',
	# 						num_aircraft = 2,
	# 						earliest_block = 7,
	# 						latest_block = 17)

	# 	student_1 = StudentFactory.create_one_block_three_days_student()
	# 	student_1.full_name = 's1'
	# 	student_2 = StudentFactory.create_one_block_three_days_student()
	# 	student_2.full_name = 's2'
		
	# 	self.free_instructor.add_student(student_1)
	# 	self.free_instructor.add_student(student_2)
	# 	schedule_builder = ScheduleBuilder(self.free_instructors, self.calendar, available_aircraft_2, test_environment=True)
	# 	status, solution_log = schedule_builder.build_schedule()
	# 	self.assertEqual(status, cp_model.INFEASIBLE)

	def test_instructor_has_one_student_at_a_given_time(self):
		available_aircraft_2 = {}
		available_aircraft_2['R22'] = self.aircraft_factory.build_aircraft_of_model(
							name_prefix = 'R22',
							model = 'R22',
							num_aircraft = 2,
							earliest_block = 7,
							latest_block = 17)

		student_1 = StudentFactory.create_one_block_three_days_student()
		student_1.full_name = 's1'
		student_2 = StudentFactory.create_one_block_three_days_student()
		student_2.full_name = 's2'
		
		self.free_instructor.add_student(student_1)
		self.free_instructor.add_student(student_2)
		schedule_builder = ScheduleBuilder(self.free_instructors, self.calendar, available_aircraft_2, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		self.assertEqual(status, cp_model.INFEASIBLE)

	# def test_instructor_has_one_student_at_a_given_time(self):
	# 	student_1_unavailability = {
	# 			'Sunday': '05:30;06:30;',
	# 			'Monday': '05:30;06:30;18:30;19:30;20:30;17:30;',
	# 			'Tuesday': '05:30;06:30;07:30;08:30;09:30;10:30;11:30;12:30;13:30;',
	# 			'Wednesday': '05:30;06:30;',
	# 			'Thursday': '05:30;06:30;',
	# 			'Friday': '05:30;06:30;',
	# 			'Saturday': '05:30;06:30;'}

	# 	student_1 = Student(first_name='Student', last_name='1', unavailability=UnavailabilityFactory.get_three_odd_blocks_three_days(), rating='Instrument', schedule_type='Fixed-Wing', instructor='I1')

	# 	student_2_unavailability = {
	# 			'Sunday': '',
	# 			'Monday': '06:30;07:30;08:30;09:30;11:30;10:30;12:30;13:30;14:30;15:30;',
	# 			'Tuesday': '06:30;07:30;08:30;09:30;11:30;10:30;12:30;13:30;',
	# 			'Wednesday': '06:30;07:30;08:30;09:30;10:30;11:30;13:30;12:30;',
	# 			'Thursday': '06:30;07:30;08:30;09:30;10:30;11:30;12:30;13:30;',
	# 			'Friday': '06:30;08:30;07:30;09:30;10:30;11:30;12:30;13:30;',
	# 			'Saturday': ''}


	# 	student_2 = Student(first_name='Student', last_name='2', unavailability=UnavailabilityFactory.get_three_odd_blocks_three_days(), rating='Private', schedule_type='Fixed-Wing', instructor='I1')

	# 	instructor_unavailability = {
	# 			'Sunday': '05:30;06:30;07:30;16:30;17:30;18:30;19:30;20:30;',
	# 			'Monday': '05:30;06:30;07:30;16:30;17:30;18:30;19:30;20:30;',
	# 			'Tuesday': '05:30;06:30;07:30;16:30;17:30;18:30;19:30;20:30;',
	# 			'Wednesday': '05:30;06:30;07:30;16:30;17:30;18:30;19:30;20:30;',
	# 			'Thursday': '05:30;06:30;07:30;16:30;17:30;18:30;19:30;20:30;',
	# 			'Friday': '05:30;06:30;07:30;08:30;09:30;10:30;11:30;12:30;13:30;14:30;15:30;16:30;17:30;18:30;19:30;20:30;',
	# 			'Saturday': '05:30;06:30;07:30;20:30;19:30;18:30;17:30;16:30;'}

	# 	instructors = {}
	# 	instructor = Instructor(first_name='I', last_name='1', unavailability=UnavailabilityFactory.get_three_odd_blocks_three_days())

	# 	instructor.add_student(student_1)
	# 	instructor.add_student(student_2)

	# 	instructors[instructor.full_name] = instructor

	# 	available_aircraft = {}
	# 	available_aircraft['C172'] = self.aircraft_factory.build_aircraft_of_model(
	# 						name_prefix = 'C172',
	# 						model = 'C172',
	# 						num_aircraft = 2,
	# 						earliest_block = 7,
	# 						latest_block = 17)
	# 	available_aircraft['FWSIM'] = self.aircraft_factory.build_aircraft_of_model(
	# 						name_prefix = 'FWSIM',
	# 						model = 'FWSIM',
	# 						num_aircraft = 1,
	# 						earliest_block = 7,
	# 						latest_block = 17)

		
	# 	schedule_builder = ScheduleBuilder(instructors, self.calendar, available_aircraft, test_environment=True)
	# 	status, solution_log = schedule_builder.build_schedule()
	# 	print()
	# 	pp.pprint(solution_log)
	# 	self.assertEqual(status, cp_model.FEASIBLE)

	# def test_if_solo_instructor_is_SOLO_FLIGHT(self):
	# 	available_aircraft_c172 = {}
	# 	available_aircraft_c172['C172'] = self.aircraft_factory.build_aircraft_of_model(
	# 						name_prefix = 'C172',
	# 						model = 'C172',
	# 						num_aircraft = 1,
	# 						earliest_block = 7,
	# 						latest_block = 17)
	# 	available_aircraft_c172['FWSIM'] = self.aircraft_factory.build_aircraft_of_model(
	# 						name_prefix = 'FWSIM',
	# 						model = 'FWSIM',
	# 						num_aircraft = 1,
	# 						earliest_block = 7,
	# 						latest_block = 17,
	# 						soloable=False)

	# 	student = StudentFactory.create_free_student(rating='Commercial', schedule_type='Fixed-Wing', instructor=self.free_instructor.full_name)

	# 	instructors = {}

	# 	primary_instructor = InstructorFactory.create_free_instructor()
	# 	primary_instructor.full_name = "Primary Instructor"
	# 	primary_instructor.add_student(student)
	# 	instructors[primary_instructor.full_name] = primary_instructor

	# 	solo_instructor_placeholder = InstructorFactory.create_free_instructor()
	# 	solo_instructor_placeholder.full_name = "SOLO FLIGHT"
	# 	solo_instructor_placeholder.solo_placeholder = True
	# 	solo_instructor_placeholder.add_student(student)
	# 	instructors[solo_instructor_placeholder.full_name] = solo_instructor_placeholder

	# 	schedule_builder = ScheduleBuilder(instructors, self.calendar, available_aircraft_c172, test_environment=True)
	# 	status, solution_log = schedule_builder.build_schedule()
	# 	print()
	# 	pp.pprint(solution_log)


	def test_pvt_rw_has_desired_flights_per_week(self):
		expected_aircraft = {'R22' : 3}
		student = StudentFactory.create_free_student(rating='Private', schedule_type='Rotor-Wing')
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, self.calendar, self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)

	def test_inst_rw_has_desired_flights_per_week(self):
		expected_aircraft = {'R44' : 2, 'RWSIM' : 1}
		student = StudentFactory.create_free_student(rating='Instrument', schedule_type='Rotor-Wing')
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, self.calendar, self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)


	def test_com_rw_has_desired_flights_per_week(self):
		expected_aircraft = {'R22' : 3}
		student = StudentFactory.create_free_student(rating='Commercial', schedule_type='Rotor-Wing')
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, self.calendar, self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)

	def test_cfi_rw_has_desired_flights_per_week(self):
		expected_aircraft = {'R22' : 2}
		student = StudentFactory.create_free_student(rating='CFI', schedule_type='Rotor-Wing')
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, self.calendar, self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)

	def test_cfii_rw_has_desired_flights_per_week(self):
		expected_aircraft = {'R44' : 1, 'RWSIM' : 1}
		student = StudentFactory.create_free_student(rating='CFII', schedule_type='Rotor-Wing')
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, self.calendar, self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)

	def test_pvt_fw_has_desired_flights_per_week(self):
		expected_aircraft = {'C172' : 3}
		student = StudentFactory.create_free_student(rating='Private', schedule_type='Fixed-Wing')
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, self.calendar, self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)

	def test_inst_fw_has_desired_flights_per_week(self):
		expected_aircraft = {'C172' : 2, 'FWSIM' : 1}
		student = StudentFactory.create_free_student(rating='Instrument', schedule_type='Fixed-Wing')
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, self.calendar, self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)

	def test_com_fw_has_desired_flights_per_week(self):
		expected_aircraft = {'C172' : 3, 'FWSIM' : 1}
		student = StudentFactory.create_free_student(rating='Commercial', schedule_type='Fixed-Wing')

		instructors = {}

		primary_instructor = InstructorFactory.create_free_instructor()
		primary_instructor.full_name = "Primary Instructor"
		primary_instructor.add_student(student)
		instructors[primary_instructor.full_name] = primary_instructor

		solo_instructor_placeholder = InstructorFactory.create_free_instructor()
		solo_instructor_placeholder.full_name = "SOLO FLIGHT"
		solo_instructor_placeholder.solo_placeholder = True
		solo_instructor_placeholder.add_student(student)
		instructors[solo_instructor_placeholder.full_name] = solo_instructor_placeholder

		schedule_builder = ScheduleBuilder(instructors, self.calendar, self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)

	def test_cfi_fw_has_desired_flights_per_week(self):
		expected_aircraft = {'C172' : 1}
		student = StudentFactory.create_free_student(rating='CFI', schedule_type='Fixed-Wing')
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, self.calendar, self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)

	def test_cfii_fw_has_desired_flights_per_week(self):
		expected_aircraft = {'C172' : 1, 'FWSIM' : 1}
		student = StudentFactory.create_free_student(rating='CFII', schedule_type='Fixed-Wing')
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, self.calendar, self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)

	def test_mei_fw_has_desired_flights_per_week(self):
		expected_aircraft = {'BARON' : 3}
		student = StudentFactory.create_free_student(rating='MEI', schedule_type='Fixed-Wing')
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, self.calendar, self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)

	def test_com_me_fw_has_desired_flights_per_week(self):
		expected_aircraft = {'BARON' : 3}
		student = StudentFactory.create_free_student(rating='ME', schedule_type='Fixed-Wing')
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, self.calendar, self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)

	def test_com_fw_has_specified_solo_flights(self):
		# This test works because only a solo instructor is created
		expected_aircraft = {'C172' : 1}
		student = StudentFactory.create_free_student(rating='Commercial', schedule_type='Fixed-Wing')

		instructors = {}

		solo_instructor_placeholder = InstructorFactory.create_free_instructor()
		solo_instructor_placeholder.full_name = "SOLO FLIGHT"
		solo_instructor_placeholder.solo_placeholder = True
		solo_instructor_placeholder.add_student(student)
		instructors[solo_instructor_placeholder.full_name] = solo_instructor_placeholder

		schedule_builder = ScheduleBuilder(instructors, self.calendar, self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)


	def test_an_instructor_student_has_no_conflicts(self):
		instructors = {}

		instructor_instructor = InstructorFactory.create_four_block_three_days_instructor(first_name='InstructorInstructor', last_name='L')
		instructor_student = InstructorStudentFactory.create_four_block_three_days_instructor_student(first_name='InstructorStudent', last_name='L', rating='MEI', schedule_type='Fixed-Wing', instructor=instructor_instructor.full_name)

		instructors[instructor_instructor.full_name] = instructor_instructor
		instructors[instructor_student.full_name] = instructor_student

		instructor_instructor_student_1 = StudentFactory.create_four_block_three_days_student(first_name='student_1', last_name='L', rating='Private', schedule_type='Fixed-Wing')
		instructor_student_student_1 = StudentFactory.create_four_block_three_days_student(first_name='student_2', last_name='L', rating='Private', schedule_type='Fixed-Wing')
		instructor_student_student_2 = StudentFactory.create_four_block_three_days_student(first_name='student_3', last_name='L', rating='Private', schedule_type='Fixed-Wing')

		instructor_instructor.add_student(instructor_student)
		instructor_instructor.add_student(instructor_instructor_student_1)
		instructor_student.add_student(instructor_student_student_1)
		instructor_student.add_student(instructor_student_student_2)

		schedule_builder = ScheduleBuilder(instructors, self.calendar, self.many_aircraft, test_environment=True)
		# print()
		status, solution_log = schedule_builder.build_schedule()
		# pp.pprint(solution_log)
		self.assertEqual(len(solution_log['individual_day_hour_block']), len(set(solution_log['individual_day_hour_block'])))





	def test_instructors_scheduled_beyond_14_hour_duty_day_infeasable(self):
		calendar = Calendar(earliest_block=0, latest_block=24)
		available_aircraft = {}
		available_aircraft['C172'] = self.aircraft_factory.build_aircraft_of_model(
										name_prefix = 'C172',
										model = 'C172',
										num_aircraft = 1,
										earliest_block = calendar.earliest_block,
										latest_block = calendar.latest_block)

		s1 = StudentFactory.create_student(first_name='s1', rating='CFI', schedule_type='Fixed-Wing', unavailability=UnavailabilityFactory.get_free_one_day_at_0000_only())
		s2 = StudentFactory.create_student(first_name='s2', rating='CFI', schedule_type='Fixed-Wing', unavailability=UnavailabilityFactory.get_free_one_day_at_1400_only())

		instructors = {}
		instructor = InstructorFactory.create_one_day_free_only_instructor()
		instructor.add_student(s1)
		instructor.add_student(s2)

		instructors[instructor.full_name] = instructor
		schedule_builder = ScheduleBuilder(instructors, calendar, available_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		self.assertEqual(status, cp_model.INFEASIBLE)

	def test_instructors_scheduled_within_14_hour_duty_day_feasable(self):
		calendar = Calendar(earliest_block=0, latest_block=24)
		available_aircraft = {}
		available_aircraft['C172'] = self.aircraft_factory.build_aircraft_of_model(
										name_prefix = 'C172',
										model = 'C172',
										num_aircraft = 1,
										earliest_block = calendar.earliest_block,
										latest_block = calendar.latest_block)

		s1 = StudentFactory.create_student(first_name='s1', rating='CFI', schedule_type='Fixed-Wing', unavailability=UnavailabilityFactory.get_free_one_day_at_0000_only())
		s2 = StudentFactory.create_student(first_name='s2', rating='CFI', schedule_type='Fixed-Wing', unavailability=UnavailabilityFactory.get_free_one_day_at_1200_only())

		instructors = {}
		instructor = InstructorFactory.create_one_day_free_only_instructor()
		instructor.add_student(s1)
		instructor.add_student(s2)

		instructors[instructor.full_name] = instructor
		schedule_builder = ScheduleBuilder(instructors, calendar, available_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		self.assertEqual(status, cp_model.FEASIBLE)
	    
	def test_a_one_hour_availability_results_in_infeasable(self):
		student = StudentFactory.create_student(first_name='s1', rating='CFI', schedule_type='Fixed-Wing', unavailability=UnavailabilityFactory.get_one_hour_free_7am())
		# s2 = StudentFactory.create_one_day_free_only_student(first_name='s2', rating='CFI', schedule_type='Fixed-Wing', unavailability=UnavailabilityFactory.get_completely_free_one_day_at_1200_only())
		self.free_instructor.add_student(student)

		schedule_builder = ScheduleBuilder(self.free_instructors, self.calendar, self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		self.assertEqual(status, cp_model.INFEASIBLE)

	def test_flights_less_than_2_hours_apart_are_infeasable(self):
		s1 = StudentFactory.create_student(first_name='s1', rating='CFI', schedule_type='Fixed-Wing', unavailability=UnavailabilityFactory.get_one_block_free_7am())
		s2 = StudentFactory.create_student(first_name='s2', rating='CFI', schedule_type='Fixed-Wing', unavailability=UnavailabilityFactory.get_one_block_free_8am())
		self.free_instructor.add_student(s1)
		self.free_instructor.add_student(s2)

		schedule_builder = ScheduleBuilder(self.free_instructors, self.calendar, self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		self.assertEqual(status, cp_model.INFEASIBLE)

	def test_flights_greater_than_2_hours_apart_are_feasable(self):
		s1 = StudentFactory.create_student(first_name='s1', rating='CFI', schedule_type='Fixed-Wing', unavailability=UnavailabilityFactory.get_one_block_free_7am())
		s2 = StudentFactory.create_student(first_name='s2', rating='CFI', schedule_type='Fixed-Wing', unavailability=UnavailabilityFactory.get_one_block_free_9am())
		self.free_instructor.add_student(s1)
		self.free_instructor.add_student(s2)

		schedule_builder = ScheduleBuilder(self.free_instructors, self.calendar, self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		self.assertTrue(status == cp_model.FEASIBLE or status == cp_model.OPTIMAL)


	def test_instructor_scheduled_for_7_days_infeasable(self):
		# must have one day off per week
		s1 = StudentFactory.create_free_student(first_name='s1', rating='CFI', schedule_type='Fixed-Wing')
		s2 = StudentFactory.create_free_student(first_name='s2', rating='CFI', schedule_type='Fixed-Wing')
		s3 = StudentFactory.create_free_student(first_name='s3', rating='CFI', schedule_type='Fixed-Wing')
		s4 = StudentFactory.create_free_student(first_name='s4', rating='CFI', schedule_type='Fixed-Wing')
		s5 = StudentFactory.create_free_student(first_name='s5', rating='CFI', schedule_type='Fixed-Wing')
		s6 = StudentFactory.create_free_student(first_name='s6', rating='CFI', schedule_type='Fixed-Wing')
		s7 = StudentFactory.create_free_student(first_name='s7', rating='CFI', schedule_type='Fixed-Wing')

		instructors = {}
		instructor = InstructorFactory.create_instructor(unavailability=UnavailabilityFactory.get_one_block_free_per_day_7am())
		instructor.add_student(s1)
		instructor.add_student(s2)
		instructor.add_student(s3)
		instructor.add_student(s4)
		instructor.add_student(s5)
		instructor.add_student(s6)
		instructor.add_student(s7)

		instructors[instructor.full_name] = instructor

		schedule_builder = ScheduleBuilder(instructors, self.calendar, self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		self.assertEqual(status, cp_model.INFEASIBLE)

	def test_instructor_scheduled_for_6_days_feasable(self):
		# must have one day off per week
		s1 = StudentFactory.create_free_student(first_name='s1', rating='CFI', schedule_type='Fixed-Wing')
		s2 = StudentFactory.create_free_student(first_name='s2', rating='CFI', schedule_type='Fixed-Wing')
		s3 = StudentFactory.create_free_student(first_name='s3', rating='CFI', schedule_type='Fixed-Wing')
		s4 = StudentFactory.create_free_student(first_name='s4', rating='CFI', schedule_type='Fixed-Wing')
		s5 = StudentFactory.create_free_student(first_name='s5', rating='CFI', schedule_type='Fixed-Wing')
		s6 = StudentFactory.create_free_student(first_name='s6', rating='CFI', schedule_type='Fixed-Wing')

		instructors = {}
		instructor = InstructorFactory.create_instructor(unavailability=UnavailabilityFactory.get_one_block_free_per_day_7am())
		instructor.add_student(s1)
		instructor.add_student(s2)
		instructor.add_student(s3)
		instructor.add_student(s4)
		instructor.add_student(s5)
		instructor.add_student(s6)

		instructors[instructor.full_name] = instructor

		schedule_builder = ScheduleBuilder(instructors, self.calendar, self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		self.assertEqual(status, cp_model.FEASIBLE)

	def test_if_an_instructor_works_6_hours_gets_break(self):
		s1 = StudentFactory.create_free_student(first_name='s1', rating='CFI', schedule_type='Fixed-Wing')
		s2 = StudentFactory.create_free_student(first_name='s2', rating='CFI', schedule_type='Fixed-Wing')
		s3 = StudentFactory.create_free_student(first_name='s3', rating='CFI', schedule_type='Fixed-Wing')
		s4 = StudentFactory.create_free_student(first_name='s4', rating='CFI', schedule_type='Fixed-Wing')

		instructors = {}
		instructor = InstructorFactory.create_instructor(unavailability=UnavailabilityFactory.get_free_10_hours_one_day_only())
		instructor.add_student(s1)
		instructor.add_student(s2)
		instructor.add_student(s3)
		instructor.add_student(s4)

		instructors[instructor.full_name] = instructor

		schedule_builder = ScheduleBuilder(instructors, self.calendar, self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		# print(status)
		# pp.pprint(solution_log)
		scheduled_blocks = sorted(solution_log['blocks'])
		consecutive_block_counter = 1 # the first block is automatically "consecutive""
		for current in range(0, len(scheduled_blocks)):
			next = current + 1
			if next < len(scheduled_blocks):
				difference = scheduled_blocks[next] - scheduled_blocks[current]
				if difference == 2:
					consecutive_block_counter += 1
		self.assertTrue(consecutive_block_counter <= 3) # must be less than 3 because 3 flights * 2 hours = 6 consecutive hours




	# def test_if_available_schedule_pvt_students_4x_week(self):
	#     assert False

	# def test_if_available_schedule_commercial_students_4x_week(self):
	#     assert False


	# def test_end_to_end_instructor_in_one_place_at_time(self):
	#     file_path = 'tests/fake_data_simple.csv'

	#     profile_builder = ProfileBuilder(file_path)
	#     fw_instructors, rw_instructors = profile_builder.build_instructor_profiles()

	#     available_aircraft = {}
	#     aircraft_factory = AircraftFactory()
	#     earliest_block = 7
	#     latest_block = 17
	#     available_aircraft['R22'] = aircraft_factory.build_aircraft_of_model(
	#                                     name_prefix = 'R22',
	#                                     model = 'R22',
	#                                     num_aircraft = 6,
	#                                     earliest_block = earliest_block,
	#                                     latest_block = latest_block)

	#     available_aircraft['R44'] = aircraft_factory.build_aircraft_of_model(
	#                                     name_prefix = 'R44',
	#                                     model = 'R44',
	#                                     num_aircraft = 3,
	#                                     earliest_block = earliest_block,
	#                                     latest_block = latest_block)

	#     available_aircraft['RWSIM'] = aircraft_factory.build_aircraft_of_model(
	#                                     name_prefix = 'RWSIM',
	#                                     model = 'RWSIM',
	#                                     num_aircraft = 1,
	#                                     earliest_block = earliest_block,
	#                                     latest_block = latest_block,
	#                                     soloable=False)

	#     available_aircraft['C172'] = aircraft_factory.build_aircraft_of_model(
	#                                     name_prefix = 'C172',
	#                                     model = 'C172',
	#                                     num_aircraft = 11,
	#                                     earliest_block = earliest_block,
	#                                     latest_block = latest_block)

	#     available_aircraft['BARON'] = aircraft_factory.build_aircraft_of_model(
	#                                     name_prefix = 'BARON',
	#                                     model = 'BARON',
	#                                     num_aircraft = 1,
	#                                     earliest_block = earliest_block,
	#                                     latest_block = latest_block)

	#     available_aircraft['FWSIM'] = aircraft_factory.build_aircraft_of_model(
	#                                     name_prefix = 'FWSIM',
	#                                     model = 'FWSIM',
	#                                     num_aircraft = 1,
	#                                     earliest_block = earliest_block,
	#                                     latest_block = latest_block,
	#                                     soloable=False)

	#     fw_schedule_builder = ScheduleBuilder(fw_instructors, self.calendar, available_aircraft, test_environment=True)
	#     fw_status, fw_solution_log = fw_schedule_builder.build_schedule()
	#     rw_schedule_builder = ScheduleBuilder(rw_instructors, self.calendar, available_aircraft, test_environment=True)
	#     rw_status, rw_solution_log = rw_schedule_builder.build_schedule()
	#     self.assertEqual(len(fw_solution_log['instructor_and_day_hour_blocks']), len(set(fw_solution_log['instructor_and_day_hour_blocks'])))
	#     self.assertEqual(len(rw_solution_log['instructor_and_day_hour_blocks']), len(set(rw_solution_log['instructor_and_day_hour_blocks'])))
	#     self.assertEqual(fw_status, cp_model.FEASIBLE)
	#     self.assertEqual(rw_status, cp_model.FEASIBLE)

if __name__ == '__main__':
	unittest.main()
