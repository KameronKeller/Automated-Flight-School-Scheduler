from models.instructor_student import InstructorStudent
from tests.factory.unavailability_factory import UnavailabilityFactory

class InstructorStudentFactory:

	first_name = 'InstructorStudent'
	last_name = 'L'

	rating = 'Private'
	schedule_type = 'Rotor-Wing'
	instructor = 'instructor'
	students = []

	@staticmethod
	def create_instructor_student(first_name=first_name, last_name=last_name, unavailability=UnavailabilityFactory.get_default_unavailability(), rating=rating, schedule_type=schedule_type, instructor=instructor, students=students):
		return InstructorStudent(first_name=first_name, last_name=last_name, unavailability=unavailability, rating=rating, schedule_type=schedule_type, instructor=instructor, students=students)

	@staticmethod
	def create_four_block_three_days_instructor_student(first_name=first_name, last_name=last_name, unavailability=UnavailabilityFactory.get_four_odd_blocks_three_days(), rating=rating, schedule_type=schedule_type, instructor=instructor, students=students):
		return InstructorStudent(first_name=first_name, last_name=last_name, unavailability=unavailability, rating=rating, schedule_type=schedule_type, instructor=instructor, students=students)
