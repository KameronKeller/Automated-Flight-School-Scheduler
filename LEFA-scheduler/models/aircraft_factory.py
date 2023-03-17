import math
from models.aircraft import Aircraft

class AircraftFactory:

	def __init__(self):
		self.aircrafts = {}

	def build_aircraft_of_model(self, name_prefix, model, num_aircraft, earliest_block, latest_block):
		later_start_time = earliest_block + 1
		earlier_finish_time = latest_block - 1
		majority_aircraft = True # flag for determining how many odd/even aircraft to make if number of aircraft is odd

		for i in range(1, num_aircraft + 1):
			aircraft_name = name_prefix + '_' + str(i)

			if i > math.ceil(num_aircraft / 2):
				majority_aircraft = False
			
			if majority_aircraft:
				block_type = self.calculate_even_or_odd(earliest_block)
				schedule_blocks = self.calculate_blocks(earliest_block, latest_block)
			else:
				block_type = self.calculate_even_or_odd(later_start_time)
				schedule_blocks = self.calculate_blocks(later_start_time, earlier_finish_time)

			aircraft = Aircraft(aircraft_name, model, block_type, schedule_blocks)
			self.aircrafts[aircraft_name] = aircraft

		return self.aircrafts


	def calculate_even_or_odd(self, earliest_block):
		if earliest_block % 2 == 0:
			return 'even'
		else:
			return 'odd'

	def calculate_blocks(self, earliest_block, latest_block):
		latest_block += 1 # make the loop inclusive
		schedule_blocks = []
		for i in range(earliest_block, latest_block, 2):
			schedule_blocks.append(i)
		return schedule_blocks






