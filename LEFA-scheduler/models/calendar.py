class Calendar:

	DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
	EARLIEST_BLOCK = 7
	LATEST_BLOCK = 17

	@classmethod
	def get_days(self):
		return Calendar.DAYS

	@classmethod
	def get_possible_blocks(self):
		return list(range(Calendar.EARLIEST_BLOCK, Calendar.LATEST_BLOCK + 1))
