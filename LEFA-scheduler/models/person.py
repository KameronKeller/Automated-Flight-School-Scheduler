class Person:

	def __init__(self, first_name, last_name, unavailability):
		self.first_name = first_name
		self.last_name = last_name
		self.full_name = first_name + ' ' + last_name
		self.unavailability = self.parse_unavailability(unavailability)
		# self.unavailability = unavailability
		# print(self.unavailability)

	def parse_unavailability(self, unavailability):
		parsed_unavailability = {}
		# print(unavailability)
		for day, times in unavailability.items():
			converted_times = []
			split_times = times.split(';')
			for time in split_times:
				if len(time) == 0:
					continue
				else:
					hour = int(time.split(':')[0])
					converted_times.append(hour)
			parsed_unavailability[day] = converted_times
			print(converted_times)

		return parsed_unavailability
