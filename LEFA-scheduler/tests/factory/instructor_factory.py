from models.instructor import Instructor
from tests.factory.unavailability_factory import UnavailabilityFactory

class InstructorFactory:

	first_name = 'Instructor'
	last_name = 'L'

	@staticmethod
	def create_instructor(first_name=first_name, last_name=last_name, unavailability=UnavailabilityFactory.get_default_unavailability()):
		return Instructor(first_name, last_name, unavailability)

	@staticmethod
	def create_free_instructor(first_name=first_name, last_name=last_name, unavailability=UnavailabilityFactory.get_completely_free()):
		return Instructor(first_name, last_name, unavailability)

	@staticmethod
	def create_unavailable_instructor(first_name=first_name, last_name=last_name, unavailability=UnavailabilityFactory.get_completely_unavailable()):
		return Instructor(first_name, last_name, unavailability)

	@staticmethod
	def create_one_block_instructor(first_name=first_name, last_name=last_name, unavailability=UnavailabilityFactory.get_one_block_free()):
		return Instructor(first_name, last_name, unavailability)

	@staticmethod
	def create_four_block_three_days_instructor(first_name=first_name, last_name=last_name, unavailability=UnavailabilityFactory.get_four_odd_blocks_three_days()):
		return Instructor(first_name=first_name, last_name=last_name, unavailability=unavailability)

	@staticmethod
	def create_one_day_free_only_instructor(first_name=first_name, last_name=last_name, unavailability=UnavailabilityFactory.get_completely_free_one_day_only()):
		return Instructor(first_name=first_name, last_name=last_name, unavailability=unavailability)
