from models.instructor_student import InstructorStudent

class InstructorStudentFactory:

	first_name = 'first'
	last_name = 'last'
	unavailability = {'fixedwing_friday_unavailability': '05:30;06:30;',
	'fixedwing_monday_unavailability': '06:30;05:30;09:30;11:30;10:30;',
	'fixedwing_saturday_unavailability': '05:30;06:30;07:30;08:30;09:30;10:30;11:30;12:30;13:30;14:30;15:30;16:30;17:30;18:30;19:30;20:30;',
	'fixedwing_sunday_unavailability': '05:30;06:30;07:30;08:30;09:30;10:30;11:30;12:30;13:30;14:30;15:30;16:30;17:30;18:30;19:30;20:30;',
	'fixedwing_thursday_unavailability': '05:30;06:30;',
	'fixedwing_tuesday_unavailability': '06:30;05:30;',
	'fixedwing_wednesday_unavailability': '05:30;06:30;'}
	rating = 'rating'
	schedule_type = 'schedule_type'
	instructor = 'instructor'
	students = ['student_1']

	@staticmethod
	def create_instructor_student(first_name=first_name, last_name=last_name, unavailability=unavailability, rating=rating, schedule_type=schedule_type, instructor=instructor, students=students):
		return InstructorStudent(first_name=first_name, last_name=last_name, unavailability=unavailability, rating=rating, schedule_type=schedule_type, instructor=instructor, students=students)
