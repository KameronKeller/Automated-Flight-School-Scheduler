from models.person import Person

class Student(Person):

	def __init__(self, first_name, last_name, unavailability, rating, schedule_type, instructor):
		super().__init__(first_name, last_name, unavailability)
		self.rating = rating
		self.schedule_type = schedule_type
		self.instructor = instructor
		self.aircraft = self.determine_aircraft(self.rating, self.schedule_type)

	def determine_aircraft(self, rating, schedule_type):
		"""
		Determines the aircraft that the student can fly based on their rating and schedule type.
		:param rating: The rating of the student, string
		:param schedule_type: The schedule type of the student, string
		"""
		type_and_rating = rating + ' ' + schedule_type
		match type_and_rating:
			case 'Instrument 1 Flight Fixed-Wing':
				return {'C172' : {'dual' : 1}}
			case 'APEX 1 Flight Fixed-Wing':
				return {'C172' : {'dual' : 1}}
			case 'APEX 2 Flight Fixed-Wing':
				return {'C172' : {'dual' : 2}}
			case 'Private Rotor-Wing':
				return {'R22' : {'dual' : 3}}
			case 'Private 2 Flight Rotor-Wing':
				return {'R22' : {'dual' : 2}}
			case 'Instrument Rotor-Wing':
				return {'R44' : {'dual' : 2}, 'RWSIM' : {'dual' : 1}}
			case 'Instrument No Sim Rotor-Wing':
				return {'R44' : {'dual' : 2}}
			case 'Commercial Rotor-Wing':
				return {'R22' : {'dual' : 3}}
			case 'CFI Rotor-Wing':
				return {'R22' : {'dual' : 2}}
			case 'CFII Rotor-Wing':
				return {'R44' : {'dual' : 1}, 'RWSIM' : {'dual' : 1}}
			case 'Private Fixed-Wing':
				return {'C172' : {'dual' : 3}}
			case 'Private 1 Flight Fixed-Wing':
				return {'C172' : {'dual' : 1}}
			case 'Private 2 Flight Fixed-Wing':
				return {'C172' : {'dual' : 2}}
			case 'Instrument Fixed-Wing':
				return {'C172' : {'dual' : 2}, 'FWSIM' : {'dual' : 1}}
			case 'Instrument No Sim Fixed-Wing':
				return {'C172' : {'dual' : 2}}
			case 'Commercial Fixed-Wing':
				return {'C172' : {'dual' : 2, 'solo' : 1}, 'FWSIM' : {'dual' : 1}}
			case 'Commercial No Sim Fixed-Wing':
				return {'C172' : {'dual' : 2, 'solo' : 1}}
			case 'Commercial 2 Flight Fixed-Wing':
				return {'C172' : {'dual' : 1, 'solo' : 1}}
			case 'CFI Fixed-Wing':
				return {'C172' : {'dual' : 1}}
			case 'CFII Fixed-Wing':
				return {'C172' : {'dual' : 1}, 'FWSIM' : {'dual' : 1}}
			case 'MEI Fixed-Wing':
				return {'BARON' : {'dual' : 3}}
			case 'ME Fixed-Wing':
				return {'BARON' : {'dual' : 3}}
			case _:
				return "ERROR NOT FOUND"


