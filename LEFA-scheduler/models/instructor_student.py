from models.person import Person

class InstructorStudent(Person):

	def __init__(self, first_name, last_name, unavailability, rating, instructor, students):
		super().__init__(first_name, last_name, unavailability)
		self.rating = rating
		self.instructor = instructor
		self.students = students

	def add_student(self, student):
		self.students.append(student)
