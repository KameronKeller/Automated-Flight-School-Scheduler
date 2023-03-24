from models.instructor import Instructor
from models.student import Student
from models.aircraft import Aircraft
from models.calendar import Calendar

class Analyzer:

	def __init__(self, instructors, calendar, available_aircraft):
		self.instructors = instructors
		self.calendar = calendar
		self.available_aircraft = available_aircraft

	def tally_weekly_aircraft_demand(self):
		weekly_aircraft_demand = {}
		for instructor in self.instructors.values():
			if not instructor.solo_placeholder:
				for student in instructor.students:
					for aircraft_model, flight_configuration in student.aircraft.items():
						flights_needed_counter = 0
						for count in flight_configuration.values():
							flights_needed_counter += count
						if aircraft_model not in weekly_aircraft_demand:
							weekly_aircraft_demand[aircraft_model] = flights_needed_counter
						else:
							weekly_aircraft_demand[aircraft_model] += flights_needed_counter
		return weekly_aircraft_demand

	def tally_weekly_aircraft_availability(self):
		weekly_aircraft_availability = {}
		for aircraft_model, aircraft_instance in self.available_aircraft.items():
			flights_available_counter = 0
			for aircraft in aircraft_instance.values():
				flights_per_day = len(aircraft.schedule_blocks)
				flights_available_counter += (flights_per_day * 7)
			if aircraft_model not in weekly_aircraft_availability:
				weekly_aircraft_availability[aircraft_model] = flights_available_counter
			else:
				weekly_aircraft_availability[aircraft_model] += flights_available_counter
		return weekly_aircraft_availability

	def check_for_sufficient_aircraft(self):
		weekly_aircraft_demand = self.tally_weekly_aircraft_demand()
		weekly_aircraft_availability = self.tally_weekly_aircraft_availability()

		for aircraft_model, count in weekly_aircraft_availability.items():
			if aircraft_model in weekly_aircraft_demand:
				available = weekly_aircraft_availability[aircraft_model]
				demand = weekly_aircraft_demand[aircraft_model]
				difference = available - demand
				if difference < 0:
					print('--- Too few {} available ---'.format(aircraft_model))
				print('{} available: {}, demand: {}, difference: {}'.format(aircraft_model, available, demand, difference))



	def check_student_availability(self):
		# get the flights needed, blocks needed, and compare to availability
		max_blocks_per_day = self.calendar.get_max_num_blocks_per_day()
		possible_blocks = self.calendar.get_possible_blocks()
		for instructor in self.instructors.values():
			for student in instructor.students:
				flights_needed_counter = 0
				for aircraft_model, flight_configuration in student.aircraft.items():
					for count in flight_configuration.values():
						flights_needed_counter += count
				# print(flights_needed_counter)
				available_blocks_counter = 0
				available_days_counter = 0
				
				combined_blocks_counter = 0
				combined_days_counter = 0
				
				for day, unavailability in student.unavailability.items():
					availability_difference = possible_blocks.difference(unavailability)
					if len(availability_difference) > 1: # if student has a block available:
						available_days_counter += 1
					for hour in availability_difference:
						next_hour = hour + 1
						if hour and next_hour in availability_difference:
							available_blocks_counter += 1

					combined_unavailability = instructor.unavailability[day].union(unavailability)
					combined_availability_difference = possible_blocks.difference(combined_unavailability)

					if len(combined_availability_difference) > 1: # if student/instructor has a block available:
						combined_days_counter += 1
					for hour in combined_availability_difference:
						next_hour = hour + 1
						if hour and next_hour in availability_difference:
							combined_blocks_counter += 1

				days_difference = available_days_counter - flights_needed_counter
				blocks_difference = available_blocks_counter - flights_needed_counter

				combined_days_difference = combined_days_counter - flights_needed_counter
				combined_blocks_difference = combined_blocks_counter - flights_needed_counter

				if days_difference < 0:
					print('{} does not have enough days available. Needs {}, has {}'.format(student.full_name, flights_needed_counter, available_days_counter))
				if blocks_difference < 0:
					print('{} does not have enough blocks available. Needs {}, has {}'.format(student.full_name, flights_needed_counter, available_blocks_counter))

				if combined_days_difference < 0:
					print('{} and {} combined do not have enough days available. Needs {}, has {}'.format(student.full_name, instructor.full_name, flights_needed_counter, combined_days_counter))
				if combined_blocks_difference < 0:
					print('{} and {} combined do not have enough blocks available. Needs {}, has {}'.format(student.full_name, instructor.full_name, flights_needed_counter, combined_blocks_counter))




