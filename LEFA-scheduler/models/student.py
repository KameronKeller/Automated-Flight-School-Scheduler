from models.person import Person

class Student(Person):

	def __init__(self, first_name, last_name, unavailability, rating, schedule_type, instructor):
		super().__init__(first_name, last_name, unavailability)
		self.rating = rating
		self.schedule_type = schedule_type
		self.instructor = instructor
		self.aircraft = self.determine_aircraft(self.rating, self.schedule_type)

	def determine_aircraft(self, rating, schedule_type):
		type_and_rating = rating + ' ' + schedule_type
		match type_and_rating:
			case 'Private Rotor-Wing':
				return {'R22' : {'dual' : 3}}
			case 'Instrument Rotor-Wing':
				return {'R44' : {'dual' : 2}, 'RWSIM' : {'dual' : 1}}
			case 'Commercial Rotor-Wing':
				return {'R22' : {'dual' : 3}}
			case 'CFI Rotor-Wing':
				return {'R22' : {'dual' : 2}}
			case 'CFII Rotor-Wing':
				return {'R44' : {'dual' : 1}, 'RWSIM' : {'dual' : 1}}
			case 'Private Fixed-Wing':
				return {'C172' : {'dual' : 3}}
			case 'Instrument Fixed-Wing':
				return {'C172' : {'dual' : 2}, 'FWSIM' : {'dual' : 1}}
			case 'Commercial Fixed-Wing':
				return {'C172' : {'dual' : 2, 'solo' : 1}, 'FWSIM' : {'dual' : 1}}
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


