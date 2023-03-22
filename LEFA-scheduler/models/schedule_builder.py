from ortools.sat.python import cp_model
from models.instructor import Instructor
from models.solution_printer import SolutionPrinter
from models.instructor_student import InstructorStudent
from models.calendar import Calendar
import pprint as pp
# from models.aircraft import Aircraft

class ScheduleBuilder:

	def __init__(self, instructors, calendar, available_aircraft, test_environment=False):
		self.instructors = instructors
		self.calendar = calendar
		self.days = self.calendar.days
		self.earliest_block = self.calendar.earliest_block
		self.latest_block = self.calendar.latest_block
		self.available_aircraft = available_aircraft
		self.model = cp_model.CpModel()
		self.schedule = {}
		self.works_day = {}
		self.duty_day = {}
		self.test_environment = test_environment
		self.all_aircraft_names = self.get_all_aircraft_names()

	def get_all_aircraft_names(self):
		all_aircraft_names = []
		for aircraft_model in self.available_aircraft.values():
			for aircraft_name in aircraft_model.keys():
				all_aircraft_names.append(aircraft_name)
		return all_aircraft_names

	def generate_model(self):
		# for tracking days off
		for day in self.days:
			for instructor in self.instructors.values():
				self.works_day[(day, instructor.full_name)] = self.model.NewBoolVar('{} {}'.format(day, instructor.full_name))


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
								if schedule_block not in combined_unavailability and next_hour not in combined_unavailability:
									if instructor.solo_placeholder and not aircraft.soloable:
										continue
									else:
										self.duty_day[(day, instructor.full_name, schedule_block)] = self.model.NewBoolVar('{} {} {}'.format(day, instructor.full_name, schedule_block))
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
										self.model.AddImplication(self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)], self.works_day[(day, instructor.full_name)])
										self.model.AddImplication(self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)], self.duty_day[(day, instructor.full_name, schedule_block)])


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
			for i in self.instructors.values(): # throw away the i, not needed
				for student in i.students:
					self.model.AddAtMostOne(
						self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)]
							for instructor in self.instructors.values()
								for aircraft_model in student.aircraft.keys()
									for aircraft in self.available_aircraft[aircraft_model].values()
										for schedule_block in aircraft.schedule_blocks
											if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule)

	def add_one_block_hold_one_student(self):
		# Each aircraft can only hold one student per block, per day
		for day in self.days:
			for instructor in self.instructors.values():
				for aircraft_type in self.available_aircraft.values():
					for aircraft_name, aircraft in aircraft_type.items():
						for schedule_block in aircraft.schedule_blocks:
							self.model.AddAtMostOne(
								self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)]
									for student in instructor.students
										if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule)

	def add_instructor_at_one_place_at_a_time_on_a_given_day(self):
		for day in self.days:
			for instructor in self.instructors.values():
				for s in instructor.students:
					for a_m in s.aircraft.keys():
						for a in self.available_aircraft[a_m].values():
							for schedule_block in a.schedule_blocks:
								self.model.AddAtMostOne(
									self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)]
										for student in instructor.students
											for aircraft_model in student.aircraft.keys()
												for aircraft in self.available_aircraft[aircraft_model].values()
													if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule)



	def add_instructor_student_at_one_place_at_a_time_on_a_given_day(self):
		for day in self.days:
			for instructor in self.instructors.values():
				# if the instructor is an InstructorStudent
				if isinstance(instructor, InstructorStudent):
					for student in instructor.students:
						for aircraft_model in student.aircraft.keys():
							for aircraft in self.available_aircraft[aircraft_model].values():
								for schedule_block in aircraft.schedule_blocks:
									# If the key is in the schedule
									if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule:
										# Iterate over the InstructorStudent's needs for the same day and schedule_block as their students
										for instructor_student_aircraft_model in instructor.aircraft.keys():
											for instructor_student_aircraft in self.available_aircraft[instructor_student_aircraft_model].values():
												# if the InstructorStudent has a key in the schedule with their own instructor at the same time as their students
												if (day, instructor.instructor, instructor.full_name, instructor_student_aircraft.name, schedule_block) in self.schedule:
													# Add the implication that the InstructorStudent is not available to their instructor for that day and time block
													self.model.AddImplication(
														self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)],
														self.schedule[(day, instructor.instructor, instructor.full_name, instructor_student_aircraft.name, schedule_block)].Not())


	def add_instructors_have_max_14_hour_duty_day(self):
		# possible_blocks = Calendar.get_possible_blocks()
		last_possible_block = 24
		possible_blocks = list(range(0, last_possible_block + 1))
		max_difference = 14
		for day in self.days:
			for instructor in self.instructors.values():
				for possible_block in possible_blocks:
					current_block = (day, instructor.full_name, possible_block)
					if current_block in self.duty_day:
						banned_blocks = []
						for i in range(possible_block + max_difference, last_possible_block + 1):
							banned_blocks.append((day, instructor.full_name, i))

						for banned_block in banned_blocks:	
							if banned_block in self.duty_day:
								self.model.AddImplication(self.duty_day[current_block], self.duty_day[banned_block].Not())
					# # other_block = (day, instructor.full_name, possible_block + max_difference)
					# # if current_block in self.duty_day:
					# 	print("current {}".format(current_block))
					# # if other_block in self.duty_day:
					# 	print("other {}".format(other_block))

		# possible_blocks = Calendar.get_possible_blocks()
		# max_difference = 12
		# # on any given day
		# for day in self.days:
		# 	# for each instructor
		# 	for instructor in self.instructors.values():
		# 		for student in instructor.students:
		# 			for aircraft_model in student.aircraft.keys():
		# 				for aircraft in self.available_aircraft[aircraft_model].values():
		# 					for schedule_block in aircraft.schedule_blocks:
		# 						for next_student in instructor.students:
		# 							# Skip over the student if they are the same student
		# 							if next_student != student:
		# 								for next_aircraft_model in next_student.aircraft.keys():
		# 									for next_aircraft in self.available_aircraft[aircraft_model].values():
		# 										for next_schedule_block in next_aircraft.schedule_blocks:
		# 											current_block = (day, instructor.full_name, student.full_name, aircraft.name, schedule_block)
		# 											other_block = (day, instructor.full_name, next_student.full_name, next_aircraft.name, next_schedule_block + max_difference)
		# 											if current_block in self.schedule:
		# 												if other_block in self.schedule:
		# 													# self.model.AddImplication(self.schedule[current_block], self.schedule[other_block].Not())
		# 													self.model.AddInverse([self.schedule[current_block]], [self.schedule[other_block]])

	def add_flights_are_2_hours(self):
		for day in self.days:
			for instructor in self.instructors.values():
				for student_1 in instructor.students:
					for student_2 in instructor.students:
						if student_1 != student_2:
							for aircraft_model_1 in student_1.aircraft.keys():
								for aircraft_1 in self.available_aircraft[aircraft_model_1].values():
									for aircraft_model_2 in student_2.aircraft.keys():
										for aircraft_2 in self.available_aircraft[aircraft_model_2].values():
											for schedule_block_1 in aircraft_1.schedule_blocks:
												# for schedule_block_2 in aircraft_2.schedule_blocks:
												current_block = (day, instructor.full_name, student_1.full_name, aircraft_1.name, schedule_block_1)
												other_block = (day, instructor.full_name, student_2.full_name, aircraft_2.name, schedule_block_1 + 1)
												if current_block in self.schedule and other_block in self.schedule:
													self.model.AddImplication(self.schedule[current_block], self.schedule[other_block].Not())


				# for aircraft_instance in self.available_aircraft.values():
				# 	for aircraft_1 in aircraft_instance.values():
				# 		for aircraft_2 in aircraft_instance.values():
				# 			if aircraft_1 != aircraft_2:
				# 				current_block = (day, instructor.full_name, )
				# 			model.AddImplication(schedule)
						# self.model.Add(
						# 	# sum(self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)]
						# 	sum(self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)] + self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block + 1)]
						# 		for student in instructor.students
						# 			for schedule_block in aircraft.schedule_blocks
						# 				if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule and (day, instructor.full_name, student.full_name, aircraft.name, schedule_block + 1) in self.schedule )
						# 					<= 1)





	def add_instructors_must_have_one_day_off_per_week(self):
		for instructor in self.instructors.values():
			self.model.Add(sum(self.works_day[(day, instructor.full_name)] for day in self.days) < 7)
		# for instructor in self.instructors.values():
		# 	for student in instructor.students:
		# 		for aircraft_model, flight_configuration in student.aircraft.items():
		# 			for aircraft in self.available_aircraft[aircraft_model].values():
		# 				for schedule_block in aircraft.schedule_blocks:
		# 					self.model.Add(sum(self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)]
		# 						for day in self.days
		# 							if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule) < 7)



	def add_constraints(self):
		self.add_specified_flights_per_week()
		self.add_all_flights_on_different_day()
		self.add_one_block_hold_one_student()
		self.add_instructor_at_one_place_at_a_time_on_a_given_day()
		self.add_instructor_student_at_one_place_at_a_time_on_a_given_day()
		self.add_instructors_have_max_14_hour_duty_day()
		self.add_flights_are_2_hours()
		self.add_instructors_must_have_one_day_off_per_week()


	def output_schedule(self):
		solver = cp_model.CpSolver()
		solver.parameters.linearization_level = 0
		solver.parameters.enumerate_all_solutions = True
		solution_printer = SolutionPrinter(self.instructors, self.days, self.available_aircraft, self.schedule, 1, self.test_environment)
		status = solver.Solve(self.model, solution_printer)
		# print('\nStatistics')
		# print('  - status         : {}'.format(status))
		# print('  - conflicts      : %i' % solver.NumConflicts())
		# print('  - branches       : %i' % solver.NumBranches())
		# print('  - wall time      : %f s' % solver.WallTime())
		# print('  - solutions found: %i' % solution_printer.solution_count())
		return status, solution_printer.solution_log


	def build_schedule(self):
		self.generate_model()
		self.add_constraints()
		return self.output_schedule()


