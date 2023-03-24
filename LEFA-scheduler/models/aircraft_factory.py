import math
from models.aircraft import Aircraft

class AircraftFactory:

	"""
	Based on the number of aircraft, the earliest and latest blocks, and the model of aircraft, this method will create a dictionary of aircraft objects.
	The aircraft block_type will be odd or even depending on the earliest block.
	The aircraft schedule_blocks will be a list of all the blocks that the aircraft can fly in.
	If there are an odd number of aircraft, more aircraft will be made with the earliest block type.
	"""
	def build_aircraft_of_model(self, name_prefix, model, num_aircraft, earliest_block, latest_block, soloable=True):
		available_aircraft = {}

		later_start_time = earliest_block + 1
		earlier_finish_time = latest_block - 1
		majority_aircraft = True # flag for determining how many odd/even aircraft to make if number of aircraft is odd

		for i in range(1, num_aircraft + 1):
			aircraft_name = name_prefix + '_' + str(i)

			# if there are an odd number of aircraft, make more aircraft with the earliest block type
			if i > math.ceil(num_aircraft / 2):
				majority_aircraft = False
			
			# Determine if the earliest block is even or odd
			if majority_aircraft:
				block_type = self.calculate_even_or_odd(earliest_block)
				schedule_blocks = self.calculate_blocks(earliest_block, latest_block)
			else:
				block_type = self.calculate_even_or_odd(later_start_time)
				schedule_blocks = self.calculate_blocks(later_start_time, earlier_finish_time)

			aircraft = Aircraft(aircraft_name, model, block_type, schedule_blocks, soloable)
			available_aircraft[aircraft_name] = aircraft

		return available_aircraft


	def calculate_even_or_odd(self, earliest_block):
		if earliest_block % 2 == 0:
			return 'even'
		else:
			return 'odd'

	# Returns a list of all the blocks that the aircraft can fly in
	def calculate_blocks(self, earliest_block, latest_block):
		latest_block += 1 # make the loop inclusive
		schedule_blocks = []
		for i in range(earliest_block, latest_block, 2):
			schedule_blocks.append(i)
		return schedule_blocks






