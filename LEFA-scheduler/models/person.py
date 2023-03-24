class Person:
	"""
	A superclass for Instructor and Student.
	"""

	def __init__(self, first_name, last_name, unavailability):
		"""
		:param first_name: The first name of the person, string
		:param last_name: The last name of the person, string
		:param unavailability: The unavailability of the person, list of ints
		"""
		self.first_name = first_name
		self.last_name = last_name
		self.full_name = first_name + ' ' + last_name
		self.unavailability = self.parse_unavailability(unavailability)

	def parse_unavailability(self, unavailability):
		"""
		Parses the unavailability of the person from a string.
		:return: The unavailability of the person, dictionary of sets of ints with days as keys
		"""
		parsed_unavailability = {}
		for day, times in unavailability.items():
			converted_times = set()
			split_times = times.split(';')
			for time in split_times:
				# If the time is empty, skip it.
				if len(time) == 0:
					continue
				# Add the time to the set.
				else:
					hour = int(time.split(':')[0])
					converted_times.add(hour)
			# Add the set of times to the dictionary.
			parsed_unavailability[day] = converted_times

		return parsed_unavailability
