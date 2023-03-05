class Person:

	def __init__(self, first_name, last_name, unavailability):
		self.first_name = first_name
		self.last_name = last_name
		# self.unavailability = self.parse_unavailability(unavailability)
		self.unavailability = unavailability

	# def parse_unavailability(self, unavailability):
	# 	parsed_unavailability = {}
	# 	for day, times in unavailability.items():
	# 		parsed_unavailability[day] = times.split(';')

	# 	return parsed_unavailability
