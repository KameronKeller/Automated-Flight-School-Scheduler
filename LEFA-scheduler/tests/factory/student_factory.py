from models.student import Student

class StudentFactory:

	first_name = 'first'
	last_name = 'last'
	unavailability = {
	'Sunday' : '05:30;06:30;',
	'Monday' : '06:30;05:30;09:30;11:30;10:30;',
	'Tuesday' : '05:30;06:30;07:30;08:30;09:30;10:30;11:30;12:30;13:30;14:30;15:30;16:30;17:30;18:30;19:30;20:30;',
	'Wednesday' : '05:30;06:30;07:30;08:30;09:30;10:30;11:30;12:30;13:30;14:30;15:30;16:30;17:30;18:30;19:30;20:30;',
	'Thursday' : '05:30;06:30;',
	'Friday' : '06:30;05:30;',
	'Saturday' : '05:30;06:30;'}
	rating = 'rating'
	schedule_type = 'schedule_type'
	instructor = 'instructor'

	@staticmethod
	def create_student(first_name=first_name, last_name=last_name, unavailability=unavailability, rating=rating, schedule_type=schedule_type, instructor=instructor):
		return Student(first_name=first_name, last_name=last_name, unavailability=unavailability, rating=rating, schedule_type=schedule_type, instructor=instructor)
