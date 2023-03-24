class Calendar:

	DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
	
	def __init__(self, earliest_block, latest_block, days=DAYS):
		self.earliest_block = earliest_block
		self.latest_block = latest_block
		self.days = days

	def get_max_num_blocks_per_day(self):
		return (self.latest_block + 2 - self.earliest_block) / 2

	def get_possible_blocks(self):
		return set(range(self.earliest_block, self.latest_block + 1))
