from ortools.sat.python import cp_model
from models.instructor import Instructor
# from models.aircraft import Aircraft

class ScheduleBuilder:

	def __init__(self, instructors, days, available_aircraft):
		self.instructors = instructors
		self.days = days
		self.available_aircraft = available_aircraft
		self.model = cp_model.CpModel()
		self.schedule = {}
		self.solo_flights = []

	def generate_model(self):
		for day in self.days:
			for instructor in self.instructors.values():
				for student in instructor.students:
					for aircraft_model, flight_configuration in student.aircraft.items():
						for aircraft in self.available_aircraft[aircraft_model].values():
							for schedule_block in aircraft.schedule_blocks:
								next_hour = schedule_block + 1 # aircraft are scheduled for 2 hours

								student_unavailability = student.unavailability[day]
								instructor_unavailability = instructor.unavailability[day]
								combined_unavailability = student_unavailability.union(instructor_unavailability)

								if 'solo' in flight_configuration:
									# if the schedule_block and next_hour are not in the unavailability set, the student is available
									if schedule_block not in student_unavailability or next_hour not in student_unavailability:
										flight_key = (day, 'SOLO FLIGHT', student.full_name, aircraft.name, schedule_block)
										self.solo_flights.append(flight_key) # keep track of solo flights for adding constraints later
										self.schedule[flight_key] = self.model.NewBoolVar('{} {} {} {} {}'.format(
																													day,
																													'SOLO FLIGHT',
																													student.full_name,
																													aircraft.name,
																													schedule_block))
										# self.model.AddImplication(self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)], self.schedule[(day, 'SOLO FLIGHT', student.full_name, aircraft.name, schedule_block)])


								else: # Currently flight configurations are always dual or solo
									if schedule_block not in combined_unavailability or next_hour not in combined_unavailability:
										self.schedule[(
													day,
													instructor.full_name,
													student.full_name,
													aircraft.name,
													schedule_block)] = self.model.NewBoolVar('{} {} {} {} {}'.format(
																													day,
																													instructor.full_name,
																													student.full_name,
																													aircraft.name,
																													schedule_block))






								# # if schedule_block in student

								# print("{} {}".format(student_unavailability, instructor_unavailability))



	# 				# how should I get the aircraft at this step?
	# 					# get it from configuration, then iterate over the type the student should be flying?
					# for aircraft in aircrafts:
	# 					for block in aircraft.blocks:
	# 						if student and instructor are free:
	# 							schedule[(
	# 								day,
	# 								instructor,
	# 								student,
	# 								aircraft,
	# 								block)] = model.NewBoolVar('block {} {} {} {} {}'.format(
	# 																					day,
	# 																					instructor,
	# 																					student,
	# 																					aircraft,
	# 																					block))






