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
