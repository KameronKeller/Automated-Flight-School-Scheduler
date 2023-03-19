from models.instructor import Instructor

class InstructorFactory:

	first_name = 'Instructor'
	last_name = 'L'
	unavailability = {
	'Sunday' : '05:30;06:30;',
	'Monday' : '06:30;05:30;09:30;11:30;10:30;',
	'Tuesday' : '05:30;06:30;07:30;08:30;09:30;10:30;11:30;12:30;13:30;14:30;15:30;16:30;17:30;18:30;19:30;20:30;',
	'Wednesday' : '05:30;06:30;07:30;08:30;09:30;10:30;11:30;12:30;13:30;14:30;15:30;16:30;17:30;18:30;19:30;20:30;',
	'Thursday' : '05:30;06:30;',
	'Friday' : '06:30;05:30;',
	'Saturday' : '05:30;06:30;'}

	completely_free = {
	'Sunday': '',
	'Monday': '',
	'Tuesday': '',
	'Wednesday': '',
	'Thursday': '',
	'Friday': '',
	'Saturday': ''}

	@staticmethod
	def create_instructor(first_name=first_name, last_name=last_name, unavailability=unavailability):
		return Instructor(first_name, last_name, unavailability)

	@staticmethod
	def create_free_instructor(first_name=first_name, last_name=last_name, unavailability=completely_free):
		return Instructor(first_name, last_name, unavailability)
