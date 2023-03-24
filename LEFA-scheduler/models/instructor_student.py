from models.student import Student

class InstructorStudent(Student):
	"""
	Handles the case where an instructor is also a student.
	"""

	def __init__(self, first_name, last_name, unavailability, rating, schedule_type, instructor, students, solo_placeholder=False):
		"""
		:param first_name: The first name of the student, string
		:param last_name: The last name of the student, string
		:param unavailability: The unavailability of the student, list of ints
		:param rating: The rating of the student, string
		:param schedule_type: The schedule type of the student, string
		:param instructor: The student's instructor, string
		:param students: the instructor's students, list of objects
		:param solo_placeholder: Whether the instructor is a solo placeholder, boolean
		"""
		super().__init__(first_name, last_name, unavailability, rating, schedule_type, instructor)
		self.students = students
		self.solo_placeholder = solo_placeholder

	def add_student(self, student):
		"""
		Adds a student to the instructor's list of students.
		:param student: The student to add, object
		"""
		self.students.append(student)
