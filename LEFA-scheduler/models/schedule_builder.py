from ortools.sat.python import cp_model
from models.instructor import Instructor
from models.solution_printer import SolutionPrinter
import pprint as pp
# from models.aircraft import Aircraft

class ScheduleBuilder:

	def __init__(self, instructors, days, available_aircraft, test_environment=False):
		self.instructors = instructors
		self.days = days
		self.available_aircraft = available_aircraft
		self.model = cp_model.CpModel()
		self.schedule = {}
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
								if schedule_block not in combined_unavailability or next_hour not in combined_unavailability:
									if instructor.solo_placeholder and not aircraft.soloable:
										continue
									else:
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

	def add_specified_flights_per_week(self):
		# Each student must have the specified number of flights per week
		for instructor in self.instructors.values():
			for student in instructor.students:
				for aircraft_model, flight_configuration in student.aircraft.items():
					# the sum of flights with a solo instructor must equal the spec
					if instructor.solo_placeholder and 'solo' in flight_configuration:
						self.model.Add(
							sum(self.schedule[day, instructor.full_name, student.full_name, aircraft.name, schedule_block]
								for day in self.days
									for aircraft in self.available_aircraft[aircraft_model].values()
										for schedule_block in aircraft.schedule_blocks
											if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule
								) == flight_configuration['solo'])
					# If the instructor is a solo instructor but solo is not in the flight configuration, skip over it
					elif instructor.solo_placeholder and 'solo' not in flight_configuration:
						continue
					# the sum of flights with a dual instructor must equal the spec
					elif not instructor.solo_placeholder and 'dual' in flight_configuration:
						self.model.Add(
							sum(self.schedule[day, instructor.full_name, student.full_name, aircraft.name, schedule_block]
								for day in self.days
									for aircraft in self.available_aircraft[aircraft_model].values()
										for schedule_block in aircraft.schedule_blocks
											if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule
								) == flight_configuration['dual'])


	def add_all_flights_on_different_day(self):
		# Each flight must be on a different day
		for day in self.days:
			for instructor in self.instructors.values():
				for student in instructor.students:
					# for aircraft_model in student.aircraft.keys():
					self.model.AddAtMostOne(self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)] for aircraft_model in student.aircraft.keys() for aircraft in self.available_aircraft[aircraft_model].values() for schedule_block in aircraft.schedule_blocks
						if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule)

	def add_one_block_hold_one_student(self):
		# Each aircraft can only hold one student per block, per day
		for day in self.days:
			for instructor in self.instructors.values():
				for aircraft_type in self.available_aircraft.values():
					for aircraft_name, aircraft in aircraft_type.items():
						for schedule_block in aircraft.schedule_blocks:
							self.model.AddAtMostOne(self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)] for student in instructor.students
								if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule)
		

	def add_constraints(self):
		self.add_specified_flights_per_week()
		self.add_all_flights_on_different_day()
		self.add_one_block_hold_one_student()



						# self.model.Add(
						# 	sum(self.schedule[day, instructor.full_name, student.full_name, aircraft.name, schedule_block]
						# 		for day in self.days
						# 			for aircraft in self.available_aircraft[aircraft_model].values()
						# 				for schedule_block in aircraft.schedule_blocks
						# 					if not aircraft.soloable

						# 					# if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule
						# 					# and not aircraft.soloable
						# 			) == 0)

					# else:
					# 	self.model.Add(
					# 		sum(self.schedule[day, instructor.full_name, student.full_name, aircraft.name, schedule_block]
					# 			for day in self.days
					# 				for aircraft_model, flight_configuration in student.aircraft.items()
					# 					for aircraft in self.available_aircraft[aircraft_model].values()
					# 						for schedule_block in aircraft.schedule_blocks
					# 							if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule
					# 				) == flight_configuration['dual'])


		# If solo is forbidden in an aircraft, no solo will take place in that aircraft
		# forbidden = self.schedule[('Monday','SOLO FLIGHT 2','Peyter Cardow','FWSIM_1',7)]
		# self.model.AddForbiddenAssignments([forbidden],[('Monday','SOLO FLIGHT 2','Peyter Cardow','FWSIM_1',7)])

		# for day in self.days:
		# 	for instructor in self.instructors.values():
		# 		for student in instructor.students:
		# 			for aircraft_model, flight_configuration in student.aircraft.items():
		# 				for aircraft in self.available_aircraft[aircraft_model].values():
		# 					if instructor.solo_placeholder and not aircraft.soloable:
		# 						for schedule_block in aircraft.schedule_blocks:
		# 							print((day, instructor.full_name, student.full_name, aircraft.name, schedule_block))
		# 							if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule:
		# 								self.model.Add(self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)] == 0)


		# self.model.Add(self.schedule[('Monday','SOLO FLIGHT 2','Peyter Cardow','FWSIM_1',7)] == 0)
		# self.model.Add(self.schedule[('Tuesday','SOLO FLIGHT 2','Peyter Cardow','FWSIM_1',7)] == 0)
		# self.model.Add(self.schedule[('Monday','SOLO FLIGHT 2','Peyter Cardow','FWSIM_1',9)] == 0)
		# self.model.Add(self.schedule[('Monday','SOLO FLIGHT 2','Peyter Cardow','FWSIM_1',11)] == 0)
		# self.model.Add(self.schedule[('Monday','SOLO FLIGHT 2','Peyter Cardow','FWSIM_1',15)] == 0)
		# self.model.Add(self.schedule[('Monday','SOLO FLIGHT 2','Peyter Cardow','FWSIM_1',17)] == 0)




# 		schedule_vars = [(day_var, instructor_var, student_var, aircraft_var, block_var) for day_var, instructor_var, student_var, aircraft_var, block_var in schedule]

# # List of forbidden assignments
# forbidden_tuples = [(0, "John Doe", "Jane Doe", "Aircraft 1", "Block 1")]

# # Add forbidden assignments to the solver
# solver.AddForbiddenAssignments(schedule_vars, forbidden_tuples)





		# ========= OLD CONSTRAINTS ================
		# # Each student must have specified number of flights per week
		# for instructor in self.instructors.values():
		# 	for student in instructor.students:
		# 		# print(student.full_name + "=======================")
		# 		for aircraft_model, flight_configuration in student.aircraft.items():
		# 			# for aircraft in self.available_aircraft[aircraft_model].values():
		# 				# print(self.available_aircraft[aircraft_model])
		# 				self.model.Add(sum(self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)] for day in self.days for aircraft in self.available_aircraft[aircraft_model].values() for schedule_block in aircraft.schedule_blocks
		# 					if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule) == flight_configuration['dual'])






	def output_schedule(self):
		solver = cp_model.CpSolver()
		solver.parameters.linearization_level = 0
		solver.parameters.enumerate_all_solutions = True
		solution_printer = SolutionPrinter(self.instructors, self.days, self.available_aircraft, self.schedule, 1, self.test_environment)
		status = solver.Solve(self.model, solution_printer)
		return status, solution_printer.solution_log


	def build_schedule(self):
		self.generate_model()
		self.add_constraints()
		return self.output_schedule()


