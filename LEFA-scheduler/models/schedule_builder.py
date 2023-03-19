from ortools.sat.python import cp_model
from models.instructor import Instructor
from models.solution_printer import SolutionPrinter
# from models.aircraft import Aircraft

class ScheduleBuilder:

	def __init__(self, instructors, days, available_aircraft, test_environment=False):
		self.instructors = instructors
		self.days = days
		self.available_aircraft = available_aircraft
		self.model = cp_model.CpModel()
		self.schedule = {}
		self.solo_flights = []
		self.test_environment = test_environment

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

								# if 'solo' in flight_configuration:
								# 	pass
								# 	# if the schedule_block and next_hour are not in the unavailability set, the student is available
								# 	if schedule_block not in student_unavailability or next_hour not in student_unavailability:
								# 		flight_key = (day, 'SOLO FLIGHT', student.full_name, aircraft.name, schedule_block)
								# 		self.solo_flights.append(flight_key) # keep track of solo flights for adding constraints later
								# 		self.schedule[flight_key] = self.model.NewBoolVar('{} {} {} {} {}'.format(
								# 																					day,
								# 																					'SOLO FLIGHT',
								# 																					student.full_name,
								# 																					aircraft.name,
								# 																					schedule_block))
								# 		# self.model.AddImplication(self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)], self.schedule[(day, 'SOLO FLIGHT', student.full_name, aircraft.name, schedule_block)])


								# else: # Currently flight configurations are always dual or solo
								if schedule_block not in combined_unavailability or next_hour not in combined_unavailability:
									# print('({}, {}, {}, {}, {})'.format(day,instructor.full_name,student.full_name,aircraft.name,schedule_block))
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


	def add_constraints(self):
		# # Instructors are not scheduled during their unavailable blocks
		# for day in self.days:
		# 	for instructor in self.instructors.values():
		# 		# for aircraft_type in self.available_aircraft.values():
		# 			# for aircraft_name, aircraft in aircraft_type.items():
		# 		self.model.Add(sum(self.schedule[(day, instructor.full_name, student.full_name, aircraft_name, schedule_block)] for student in instructor.students for aircraft_type in self.available_aircraft.values() for aircraft_name, aircraft in aircraft_type.items() for schedule_block in instructor.unavailability 
		# 			if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule) == 0)
		# 					# self.model.Add(sum(self.schedule[(day, instructor.full_name, student.full_name, aircraft_name, schedule_block)] for student in instructor.students for schedule_block in instructor.unavailability 
		# 					# 	if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule) == 0)

		# 	# EXAMPLE:
		#   # Availability restriction for s1
  		# 	# model.Add(sum(flight[('John', 's1', k, '8am_to_10am')] for k in aircrafts) + sum(flight[('Emily', 's1', k, '8am_to_10am')] for k in aircrafts) == 0)

		# # Students are not scheduled during their unavailable blocks
		# for day in self.days:
		# 	for instructor in self.instructors.values():
		# 		for student in instructor.students:
		# 			for aircraft_model, flight_configuration in student.aircraft.items():
		# 				for aircraft in self.available_aircraft[aircraft_model].values():
		# 					self.model.Add(sum(self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)] for schedule_block in aircraft.schedule_blocks) == 0)
		# 					# for schedule_block in aircraft.schedule_blocks: 
		# 						# self.model.AddForbiddenAssignments()

		# for day in self.days:
		# 	for instructor in self.instructors.values():
		# 		for student in instructor.students:
		# # 		for aircraft_type in self.available_aircraft.values():
		# # 			for aircraft_name, aircraft in aircraft_type.items():
		# 					self.model.Add(sum(self.schedule[(day, instructor.full_name, student.full_name, aircraft_name, schedule_block)] for student in instructor.students for aircraft_type in self.available_aircraft.values() for aircraft_name, aircraft in aircraft_type.items() for schedule_block in student.unavailability
		# 						if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule) == 0)

		# Each student must have specified number of flights per week
		for instructor in self.instructors.values():
			for student in instructor.students:
				# print(student.full_name + "=======================")
				for aircraft_model, flight_configuration in student.aircraft.items():
					# for aircraft in self.available_aircraft[aircraft_model].values():
						# print(self.available_aircraft[aircraft_model])
						self.model.Add(sum(self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)] for day in self.days for aircraft in self.available_aircraft[aircraft_model].values() for schedule_block in aircraft.schedule_blocks
							if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule) == flight_configuration['dual'])


		# Each flight must be on a different day
		for day in self.days:
			for instructor in self.instructors.values():
				for student in instructor.students:
					# for aircraft_model in student.aircraft.keys():
					self.model.AddAtMostOne(self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)] for aircraft_model in student.aircraft.keys() for aircraft in self.available_aircraft[aircraft_model].values() for schedule_block in aircraft.schedule_blocks
						if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule)


		# Each aircraft can only hold one person per block, per day
		for day in self.days:
			for instructor in self.instructors.values():
				for aircraft_type in self.available_aircraft.values():
					for aircraft_name, aircraft in aircraft_type.items():
						for schedule_block in aircraft.schedule_blocks:
							self.model.AddAtMostOne(self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)] for student in instructor.students
								if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule)
			# for aircraft in self.available_aircraft.values():
				# print(aircraft)

	def output_schedule(self):
		solver = cp_model.CpSolver()
		solver.parameters.linearization_level = 0
		solver.parameters.enumerate_all_solutions = True
		solution_printer = SolutionPrinter(self.instructors, self.days, self.available_aircraft, self.schedule, 1, self.test_environment)
		status = solver.Solve(self.model, solution_printer)
		return status, solution_printer.solution_log
		# # Statistics.
		# print('\nStatistics')
		# print('  - status         : {}'.format(status))
		# print('  - conflicts      : %i' % solver.NumConflicts())
		# print('  - branches       : %i' % solver.NumBranches())
		# print('  - wall time      : %f s' % solver.WallTime())
		# print('  - solutions found: %i' % solution_printer.solution_count())


