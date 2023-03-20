import unittest
from ortools.sat.python import cp_model
from models.schedule_builder import ScheduleBuilder
from models.instructor import Instructor
from tests.factory.instructor_factory import InstructorFactory
from tests.factory.student_factory import StudentFactory
from models.aircraft_factory import AircraftFactory
from models.student import Student
from models.calendar import Calendar

class TestScheduleBuilder(unittest.TestCase):

    def setUp(self):
        self.free_instructor = InstructorFactory.create_free_instructor()
        self.free_instructors = {self.free_instructor.full_name : self.free_instructor}
        self.available_aircraft = {}
        self.aircraft_factory = AircraftFactory()
        self.available_aircraft['R22'] = self.aircraft_factory.build_aircraft_of_model(
                                    name_prefix = 'R22',
                                    model = 'R22',
                                    num_aircraft = 1,
                                    earliest_block = 7,
                                    latest_block = 17)
        # self.instructor = Instructor('first', 'last', 'unavailable')
    #     # self.aircraft = Aircraft()
    #     self.schedule_builder = ScheduleBuilder([self.instructor])

    # def test_attributes(self):
    #     self.assertEqual(self.schedule_builder.instructors, [self.instructor])

    # def test_flights_not_scheduled_when_student_unavailable(self):

    # def test_flights_not_scheduled_when_instructor_unavailable(self):

    def test_student_has_one_flight_per_day_max(self):
        # student_unavailability = { # only free from 9-13 Sun-Tues
        #     'Sunday' : '05:00;06:00;07:00;08:00;13:00;14:00;15:00;16:00;17:00;18:00;19:00;20:00;',
        #     'Monday' : '05:00;06:00;07:00;08:00;13:00;14:00;15:00;16:00;17:00;18:00;19:00;20:00;',
        #     'Tuesday' : '05:00;06:00;07:00;08:00;13:00;14:00;15:00;16:00;17:00;18:00;19:00;20:00;',
        #     'Wednesday' : '05:00;06:00;07:00;08:00;09:00;10:00;11:00;12:00;13:00;14:00;15:00;16:00;17:00;18:00;19:00;20:00;',
        #     'Thursday' : '05:00;06:00;07:00;08:00;09:00;10:00;11:00;12:00;13:00;14:00;15:00;16:00;17:00;18:00;19:00;20:00;',
        #     'Friday' : '05:00;06:00;07:00;08:00;09:00;10:00;11:00;12:00;13:00;14:00;15:00;16:00;17:00;18:00;19:00;20:00;',
        #     'Saturday' : '05:00;06:00;07:00;08:00;09:00;10:00;11:00;12:00;13:00;14:00;15:00;16:00;17:00;18:00;19:00;20:00;'}

        # student = Student('Student', 'L', student_unavailability, 'Private', 'Rotor-Wing', self.free_instructor.full_name)
        student = StudentFactory.create_three_blocks_three_days_student(first_name='Student', last_name='L', rating='Private', schedule_type='Rotor-Wing', instructor=self.free_instructor.full_name)
        self.free_instructor.add_student(student)
        schedule_builder = ScheduleBuilder(self.free_instructors, Calendar.get_days(), self.available_aircraft, test_environment=True)
        status, solution_log = schedule_builder.build_schedule()
        # print(solution_log)
        # print(student.unavailability)
        # self.assertIn('Sunday', solution_log['days'])
        # self.assertIn('Monday', solution_log['days'])
        # self.assertIn('Tuesday', solution_log['days'])
        self.assertTrue(len(solution_log['days']) == len(set(solution_log['days'])))
        self.assertEqual(status, cp_model.FEASIBLE)

    def test_only_one_free_block_results_in_infeasable(self):
        student = StudentFactory.create_one_block_student(first_name='Student', last_name='L', rating='Private', schedule_type='Rotor-Wing', instructor=self.free_instructor.full_name)
        self.free_instructor.add_student(student)
        schedule_builder = ScheduleBuilder(self.free_instructors, Calendar.get_days(), self.available_aircraft, test_environment=True)
        status, solution_log = schedule_builder.build_schedule()
        self.assertTrue(len(solution_log['days']) == len(set(solution_log['days'])))
        self.assertEqual(status, cp_model.INFEASIBLE)


    # def test_instructor_has_one_student_at_a_given_time(self):


    # def test_solo_students_have_no_instructor(self):
    #     assert False

    # def test_student_can_only_be_at_on_place_at_a_time(self):
    #     assert False

    # def test_student_has_desired_num_flights_per_week(self):
    #     assert False

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
