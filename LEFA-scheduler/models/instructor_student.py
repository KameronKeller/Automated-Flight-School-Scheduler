from models.student import Student

class InstructorStudent(Student):
	def __init__(self, first_name, last_name, unavailability, rating, schedule_type, instructor, students):
		super().__init__(first_name, last_name, unavailability, rating, schedule_type, instructor)
		self.students = students

	def add_student(self, student):
		self.students.append(student)
