from ortools.sat.python import cp_model
from models.instructor import Instructor
from models.solution_printer import SolutionPrinter
from models.instructor_student import InstructorStudent
from models.calendar import Calendar
import pprint as pp
# from models.aircraft import Aircraft

class ScheduleBuilder:
	"""
	Builds a schedule for the given instructors, calendar, and available aircraft.
	"""

	def __init__(self, instructors, calendar, available_aircraft, time_limit=False, test_environment=False, prescheduled_blocks=None):
		"""
		:param instructors: A dictionary of instructors, key is instructor name, value is Instructor object
		:param calendar: A Calendar object
		:param available_aircraft: A dictionary of aircraft, key is aircraft name, value is Aircraft object
		:param time_limit: The time limit for the solver in seconds, int
		:param test_environment: Whether the schedule builder is being used in a test environment, boolean
		"""
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
		self.time_limit = time_limit
		self.solution_keys = None
		self.prescheduled_blocks = prescheduled_blocks

	def get_all_aircraft_names(self):
		"""
		Returns a list of all aircraft names
		"""
		all_aircraft_names = []
		for aircraft_model in self.available_aircraft.values():
			for aircraft_name in aircraft_model.keys():
				all_aircraft_names.append(aircraft_name)
		return all_aircraft_names

	def generate_model(self):
		"""
		Generates the model for the schedule.
		"""

		# for tracking days off
		for day in self.days:
			for instructor in self.instructors.values():
				self.works_day[(day, instructor.full_name)] = self.model.NewBoolVar('{} {}'.format(day, instructor.full_name))

		# Iterate through each day, instructor, and student to create the duty day and schedule variables
		for day in self.days:
			for instructor in self.instructors.values():
				for student in instructor.students:
					for aircraft_model, flight_configuration in student.aircraft.items():
						for aircraft in self.available_aircraft[aircraft_model].values():
							for schedule_block in aircraft.schedule_blocks:

								# If this block has been prescheduled, skip it 
								if self.prescheduled_blocks is not None and (day, aircraft.name, schedule_block) in self.prescheduled_blocks:
									continue

								next_hour = schedule_block + 1 # aircraft are scheduled for 2 hours

								student_unavailability = student.unavailability[day]
								instructor_unavailability = instructor.unavailability[day]
								combined_unavailability = student_unavailability.union(instructor_unavailability)
								# If the instructor and student are available, create the duty day and schedule variables
								if schedule_block not in combined_unavailability and next_hour not in combined_unavailability:


									# If the instructor is a solo placeholder and the aircraft is not soloable, skip
									if instructor.solo_placeholder and not aircraft.soloable:
										continue
									# Otherwise, create the duty day, schedule, and works day variables
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
										# Add the implication that if the instructor is scheduled to work, they are working on that day
										self.model.AddImplication(self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)], self.works_day[(day, instructor.full_name)])
										# Add the implication that if the instructor is scheduled to work at a certain time, they are working that day at that time
										self.model.AddImplication(self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)], self.duty_day[(day, instructor.full_name, schedule_block)])


	def add_specified_flights_per_week(self):
		"""
		Add the constraint that each student must have the specified number of flights per week.
		"""

		# Each student must have the specified number of flights per week
		for instructor in self.instructors.values():
			for student in instructor.students:
				for aircraft_model, flight_configuration in student.aircraft.items():
					# the sum of flights with a solo instructor must equal the spec
					if instructor.solo_placeholder and 'solo' in flight_configuration:
						# The sum of solo flights during a week must equal the spec 
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
					# Add at most one flight per day for a student
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
			# for instructor in self.instructors.values():
				for aircraft_type in self.available_aircraft.values():
					for aircraft_name, aircraft in aircraft_type.items():
						for schedule_block in aircraft.schedule_blocks:
							# Add at most one student per block per aircraft per day
							self.model.AddAtMostOne(
								self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)]
									for instructor in self.instructors.values()
										for student in instructor.students
											if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule)

	def add_instructor_at_one_place_at_a_time_on_a_given_day(self):
		# Each instructor can only be at one place at a time on a given day
		for day in self.days:
			for instructor in self.instructors.values():
				for s in instructor.students:
					for a_m in s.aircraft.keys():
						for a in self.available_aircraft[a_m].values():
							for schedule_block in a.schedule_blocks:
								# Add at most one student per block per aircraft per day for each instructor
								self.model.AddAtMostOne(
									self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)]
										for student in instructor.students
											for aircraft_model in student.aircraft.keys()
												for aircraft in self.available_aircraft[aircraft_model].values()
													if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule)



	def add_instructor_student_at_one_place_at_a_time_on_a_given_day(self):
		# Each InstructorStudent can only be at one place at a time on a given day
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
		# Each instructor can only have a max of 14 hours of duty per day
		# possible_blocks = Calendar.get_possible_blocks()
		# last_possible_block = 24
		last_possible_block = self.calendar.latest_block
		possible_blocks = list(range(self.earliest_block, last_possible_block + 1))
		max_difference = 14
		for day in self.days:
			for instructor in self.instructors.values():
				# Iterate over all possible blocks
				for possible_block in possible_blocks:
					current_block = (day, instructor.full_name, possible_block)
					# If the current block is in the duty_day dictionary
					if current_block in self.duty_day:
						banned_blocks = []
						# Identify and track the blocks that are not allowed for the instructor
						for i in range(possible_block + max_difference, last_possible_block + 1):
							banned_blocks.append((day, instructor.full_name, i))
						# For each of the banned blocks, add the implication that the current block is not allowed if the banned block is allowed
						for banned_block in banned_blocks:	
							if banned_block in self.duty_day:
								self.model.AddImplication(self.duty_day[current_block], self.duty_day[banned_block].Not())


	def add_flights_are_2_hours(self):
		# Each flight must be 2 hours
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
													# Add the implication that the current block is not allowed if the other block is allowed
													self.model.AddImplication(self.schedule[current_block], self.schedule[other_block].Not())



	def add_instructors_must_have_one_day_off_per_week(self):
		# Instructor must have one day off per week
		for instructor in self.instructors.values():
			self.model.Add(sum(self.works_day[(day, instructor.full_name)] for day in self.days) < 7)


	def add_working_6_hours_results_in_a_break(self):
		possible_blocks = list(range(self.earliest_block, self.latest_block + 1))
		# print(possible_blocks)
		for day in self.days:
			for instructor in self.instructors.values():
				for possible_block in possible_blocks:
					# Create an sliding 8 hour window to check if the instructor is working more than 6 hours
					consecutive_blocks_window = [possible_block, possible_block + 2, possible_block + 4, possible_block + 6]
					# The sum of the schedule blocks in the window must be less than 3
					self.model.Add(sum(self.schedule[day, instructor.full_name, student.full_name, aircraft.name, schedule_block] 
						for student in instructor.students
							for aircraft_model in student.aircraft.keys()
								for aircraft in self.available_aircraft[aircraft_model].values() 
									for schedule_block in consecutive_blocks_window
										if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule) <= 3)


	def add_constraints(self):
		# Add all of the constraints
		self.add_specified_flights_per_week()
		self.add_all_flights_on_different_day()
		self.add_one_block_hold_one_student()
		self.add_instructor_at_one_place_at_a_time_on_a_given_day()
		self.add_instructor_student_at_one_place_at_a_time_on_a_given_day()
		self.add_instructors_have_max_14_hour_duty_day()
		self.add_flights_are_2_hours()
		self.add_instructors_must_have_one_day_off_per_week()
		self.add_working_6_hours_results_in_a_break()


	def output_schedule(self):
		"""
		Outputs the schedule to the console
		Returns: the status of the solver and the solution log
		"""
		solver = cp_model.CpSolver()
		solver.parameters.linearization_level = 0
		solver.parameters.enumerate_all_solutions = True
		if self.time_limit:
			solver.parameters.max_time_in_seconds = self.time_limit
		# Create a solution printer and pass it to the solver.
		solution_printer = SolutionPrinter(self.instructors, self.days, self.available_aircraft, self.schedule, 1, self.test_environment)
		status = solver.Solve(self.model, solution_printer)
		# if not self.test_environment:
		# 	print('\nStatistics')
		# 	print('  - status         : {}'.format(status))
		# 	print('  - conflicts      : %i' % solver.NumConflicts())
		# 	print('  - branches       : %i' % solver.NumBranches())
		# 	print('  - wall time      : %f s' % solver.WallTime())
		# 	print('  - solutions found: %i' % solution_printer.solution_count())
		self.solution_keys = solution_printer.solution_keys
		return status, solution_printer.solution_log

	def build_schedule(self):
		"""
		Builds the schedule and returns the status of the solver and the solution log
		"""
		self.generate_model()
		# print('generating model complete')
		self.add_constraints()
		# print('adding constraints complete')
		return self.output_schedule()


