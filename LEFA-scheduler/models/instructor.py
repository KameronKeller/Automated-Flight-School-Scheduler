from models.person import Person

class Instructor(Person):

	def __init__(self, first_name, last_name, unavailability, solo_placeholder=False):
		"""
		:param first_name: The first name of the instructor, string
		:param last_name: The last name of the instructor, string
		:param unavailability: The unavailability of the instructor, list of ints
		:param solo_placeholder: Whether the instructor is a solo placeholder, boolean
		"""
		super().__init__(first_name, last_name, unavailability)
		self.students = []
		self.solo_placeholder = solo_placeholder

	def add_student(self, student):
		"""
		Adds a student to the instructor's list of students.
		"""
		self.students.append(student)
