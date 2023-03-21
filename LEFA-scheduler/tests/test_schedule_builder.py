import unittest
from ortools.sat.python import cp_model
from models.schedule_builder import ScheduleBuilder
from models.instructor import Instructor
from tests.factory.instructor_factory import InstructorFactory
from tests.factory.student_factory import StudentFactory
from models.aircraft_factory import AircraftFactory
from models.student import Student
from models.calendar import Calendar
import pprint as pp
from collections import Counter

class TestScheduleBuilder(unittest.TestCase):

	def setUp(self):
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
		schedule_builder = ScheduleBuilder(self.unavailable_instructors, Calendar.get_days(), self.available_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		self.assertEqual(status, cp_model.INFEASIBLE)

	def test_flights_not_scheduled_when_student_unavailable(self):
		student = StudentFactory.create_free_student()
		self.unavailable_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.unavailable_instructors, Calendar.get_days(), self.available_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		self.assertEqual(status, cp_model.INFEASIBLE)

	def test_student_has_one_flight_per_day_max(self):
		student = StudentFactory.create_three_blocks_three_days_student(first_name='Student', last_name='L', rating='Private', schedule_type='Rotor-Wing', instructor=self.free_instructor.full_name)
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, Calendar.get_days(), self.available_aircraft, test_environment=True)
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

		schedule_builder = ScheduleBuilder(instructors, Calendar.get_days(), available_aircraft_c172, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		self.assertTrue(len(solution_log['days']) == len(set(solution_log['days'])))
		self.assertEqual(status, cp_model.FEASIBLE)


	def test_student_has_only_one_free_block_results_in_infeasable(self):
		# student requires 3 flights
		student = StudentFactory.create_one_block_student(first_name='Student', last_name='L', rating='Private', schedule_type='Rotor-Wing', instructor=self.free_instructor.full_name)
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, Calendar.get_days(), self.available_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		self.assertEqual(status, cp_model.INFEASIBLE)

	def test_instructor_has_only_one_free_block_results_in_infeasable(self):
		# student requires 3 flights
		student = StudentFactory.create_free_student()
		self.one_block_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.one_block_instructors, Calendar.get_days(), self.available_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		self.assertEqual(status, cp_model.INFEASIBLE)

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
		schedule_builder = ScheduleBuilder(self.free_instructors, Calendar.get_days(), available_aircraft_2, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		self.assertEqual(status, cp_model.INFEASIBLE)

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

	# 	schedule_builder = ScheduleBuilder(instructors, Calendar.get_days(), available_aircraft_c172, test_environment=True)
	# 	status, solution_log = schedule_builder.build_schedule()
	# 	print()
	# 	pp.pprint(solution_log)


	def test_pvt_rw_has_desired_flights_per_week(self):
		expected_aircraft = {'R22' : 3}
		student = StudentFactory.create_free_student(rating='Private', schedule_type='Rotor-Wing')
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, Calendar.get_days(), self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)

	def test_inst_rw_has_desired_flights_per_week(self):
		expected_aircraft = {'R44' : 2, 'RWSIM' : 1}
		student = StudentFactory.create_free_student(rating='Instrument', schedule_type='Rotor-Wing')
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, Calendar.get_days(), self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)


	def test_com_rw_has_desired_flights_per_week(self):
		expected_aircraft = {'R22' : 3}
		student = StudentFactory.create_free_student(rating='Commercial', schedule_type='Rotor-Wing')
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, Calendar.get_days(), self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)

	def test_cfi_rw_has_desired_flights_per_week(self):
		expected_aircraft = {'R22' : 2}
		student = StudentFactory.create_free_student(rating='CFI', schedule_type='Rotor-Wing')
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, Calendar.get_days(), self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)

	def test_cfii_rw_has_desired_flights_per_week(self):
		expected_aircraft = {'R44' : 1, 'RWSIM' : 1}
		student = StudentFactory.create_free_student(rating='CFII', schedule_type='Rotor-Wing')
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, Calendar.get_days(), self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)

	def test_pvt_fw_has_desired_flights_per_week(self):
		expected_aircraft = {'C172' : 3}
		student = StudentFactory.create_free_student(rating='Private', schedule_type='Fixed-Wing')
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, Calendar.get_days(), self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)

	def test_inst_fw_has_desired_flights_per_week(self):
		expected_aircraft = {'C172' : 2, 'FWSIM' : 1}
		student = StudentFactory.create_free_student(rating='Instrument', schedule_type='Fixed-Wing')
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, Calendar.get_days(), self.many_aircraft, test_environment=True)
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

		schedule_builder = ScheduleBuilder(instructors, Calendar.get_days(), self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)

	def test_cfi_fw_has_desired_flights_per_week(self):
		expected_aircraft = {'C172' : 1}
		student = StudentFactory.create_free_student(rating='CFI', schedule_type='Fixed-Wing')
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, Calendar.get_days(), self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)

	def test_cfii_fw_has_desired_flights_per_week(self):
		expected_aircraft = {'C172' : 1, 'FWSIM' : 1}
		student = StudentFactory.create_free_student(rating='CFII', schedule_type='Fixed-Wing')
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, Calendar.get_days(), self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)

	def test_mei_fw_has_desired_flights_per_week(self):
		expected_aircraft = {'BARON' : 3}
		student = StudentFactory.create_free_student(rating='MEI', schedule_type='Fixed-Wing')
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, Calendar.get_days(), self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)

	def test_com_me_fw_has_desired_flights_per_week(self):
		expected_aircraft = {'BARON' : 3}
		student = StudentFactory.create_free_student(rating='ME', schedule_type='Fixed-Wing')
		self.free_instructor.add_student(student)
		schedule_builder = ScheduleBuilder(self.free_instructors, Calendar.get_days(), self.many_aircraft, test_environment=True)
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

		schedule_builder = ScheduleBuilder(instructors, Calendar.get_days(), self.many_aircraft, test_environment=True)
		status, solution_log = schedule_builder.build_schedule()
		flight_counts = dict(Counter(solution_log['aircraft_model']))
		self.assertEqual(expected_aircraft, flight_counts)
		self.assertEqual(status, cp_model.FEASIBLE)

  

	# def test_an_instructor_student_has_no_conflicts(self):
	#     assert False

	# def test_instructors_have_less_than_14_hour_duty_day(self):
	#     assert False

	# def test_instructors_have_at_least_one_day_off_per_week(self):
	#     assert False

	# def test_if_available_schedule_pvt_students_4x_week(self):
	#     assert False

	# def test_if_available_schedule_commercial_students_4x_week(self):
	#     assert False

	# def test student availability (if they are only available at 8am, they can't be scheduled for 7-9)

	# def test_students_are_scheduled_in_proper_aircraft(self):

if __name__ == '__main__':
	unittest.main()
