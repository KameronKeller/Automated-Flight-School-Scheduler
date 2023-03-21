from models.student import Student
from tests.factory.unavailability_factory import UnavailabilityFactory

class StudentFactory:

	first_name = 'Student'
	last_name = 'L'
	rating = 'Private'
	schedule_type = 'Rotor-Wing'
	instructor = 'instructor'

	@staticmethod
	def create_student(first_name=first_name, last_name=last_name, unavailability=UnavailabilityFactory.get_default_unavailability(), rating=rating, schedule_type=schedule_type, instructor=instructor):
		return Student(first_name=first_name, last_name=last_name, unavailability=unavailability, rating=rating, schedule_type=schedule_type, instructor=instructor)

	@staticmethod
	def create_free_student(first_name=first_name, last_name=last_name, unavailability=UnavailabilityFactory.get_completely_free(), rating=rating, schedule_type=schedule_type, instructor=instructor):
		return Student(first_name=first_name, last_name=last_name, unavailability=unavailability, rating=rating, schedule_type=schedule_type, instructor=instructor)

	@staticmethod
	def create_three_blocks_three_days_student(first_name=first_name, last_name=last_name, unavailability=UnavailabilityFactory.get_three_odd_blocks_three_days(), rating=rating, schedule_type=schedule_type, instructor=instructor):
		return Student(first_name=first_name, last_name=last_name, unavailability=unavailability, rating=rating, schedule_type=schedule_type, instructor=instructor)

	@staticmethod
	def create_one_block_student(first_name=first_name, last_name=last_name, unavailability=UnavailabilityFactory.get_one_block_free(), rating=rating, schedule_type=schedule_type, instructor=instructor):
		return Student(first_name=first_name, last_name=last_name, unavailability=unavailability, rating=rating, schedule_type=schedule_type, instructor=instructor)

	@staticmethod
	def create_one_block_three_days_student(first_name=first_name, last_name=last_name, unavailability=UnavailabilityFactory.get_one_odd_block_three_days(), rating=rating, schedule_type=schedule_type, instructor=instructor):
		return Student(first_name=first_name, last_name=last_name, unavailability=unavailability, rating=rating, schedule_type=schedule_type, instructor=instructor)
