from models.person import Person

class Instructor(Person):

	def __init__(self, first_name, last_name, unavailability, solo_placeholder=False):
		super().__init__(first_name, last_name, unavailability)
		self.students = []
		self.solo_placeholder = solo_placeholder

	def add_student(self, student):
		self.students.append(student)
