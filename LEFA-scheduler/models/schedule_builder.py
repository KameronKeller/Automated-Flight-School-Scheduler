from ortools.sat.python import cp_model
from models.instructor import Instructor
from models.solution_printer import SolutionPrinter
from models.instructor_student import InstructorStudent
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
								# if isinstance(instructor, InstructorStudent):
								# 	self.model.AddImplication(
								# 		(self.schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)]
								# 			for student in instructor.students
								# 				for aircraft_model in student.aircraft.keys()
								# 					for aircraft in self.available_aircraft[aircraft_model].values()
								# 						if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule),
								# 		(self.schedule[(day, instructor_instructor.full_name, instructor.full_name, aircraft.name, schedule_block)].Not() # an instructor_instructor is the instructor of an InstructorStudent
								# 			for instructor_instructor in self.instructors.values()
								# 				for aircraft_model in instructor.aircraft.keys()
								# 					for aircraft in self.available_aircraft[aircraft_model].values()
								# 						if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self.schedule))



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




	def add_constraints(self):
		self.add_specified_flights_per_week()
		self.add_all_flights_on_different_day()
		self.add_one_block_hold_one_student()
		self.add_instructor_at_one_place_at_a_time_on_a_given_day()
		self.add_instructor_student_at_one_place_at_a_time_on_a_given_day()


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


