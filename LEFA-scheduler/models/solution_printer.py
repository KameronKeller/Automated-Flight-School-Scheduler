from ortools.sat.python import cp_model

class SolutionPrinter(cp_model.CpSolverSolutionCallback):

	# def __init__(self, schedule, days, students, aircraft, hourly_blocks, limit):
	def __init__(self, instructors, days, available_aircraft, schedule, limit, test_environment=False):
		cp_model.CpSolverSolutionCallback.__init__(self)
		self._instructors = instructors
		self._days = days
		self._available_aircraft = available_aircraft
		self._schedule = schedule
		self._solution_limit = limit
		self._solution_count = 0
		self.test_environment = test_environment
		self.solution_log = { # solution log for testing
			'days' : [],
			'instructors' : [],
			'students' : [],
			'aircraft' : [],
			'aircraft_model' : [],
			'blocks' : [],
			'day_and_hour_blocks' : [],
			'instructor_and_day_hour_blocks' : [],
			'individual_day_hour_block' : []
		}

	def on_solution_callback(self):
		# solution_log = { # solution log for testing
		# 	'days' : set(),
		# 	'instructors' : set(),
		# 	'students' : set(),
		# 	'aircraft' : set(),
		# 	'blocks' : set(),
		# 	'day_and_hour_blocks' : set()
		# }
		self._solution_count += 1
		for day in self._days:
			for instructor in self._instructors.values():
				for student in instructor.students:
					for aircraft_model, flight_configuration in student.aircraft.items():
						for aircraft in self._available_aircraft[aircraft_model].values():
							for schedule_block in aircraft.schedule_blocks:
								if (day, instructor.full_name, student.full_name, aircraft.name, schedule_block) in self._schedule: # if the block is in the schedule
									if self.Value(self._schedule[(day, instructor.full_name, student.full_name, aircraft.name, schedule_block)]): # if the value is true (valid solution)

										self.solution_log['days'].append(day)
										self.solution_log['instructors'].append(instructor.full_name)
										self.solution_log['students'].append(student.full_name)
										self.solution_log['aircraft'].append(aircraft.name)
										self.solution_log['aircraft_model'].append(aircraft_model)
										self.solution_log['blocks'].append(schedule_block)
										self.solution_log['day_and_hour_blocks'].append(day + '_' + str(schedule_block))
										self.solution_log['instructor_and_day_hour_blocks'].append(instructor.full_name + '_' + day + '_' + str(schedule_block))
										self.solution_log['individual_day_hour_block'].append(instructor.full_name + '_' + day + '_' + str(schedule_block))
										self.solution_log['individual_day_hour_block'].append(student.full_name + '_' + day + '_' + str(schedule_block))

										if not self.test_environment:
											print('{},{},{},{},{}'.format(day, instructor.full_name, student.full_name, aircraft.name, schedule_block))
		if self._solution_count >= self._solution_limit:
			if not self.test_environment:
				print('Stop search after %i solutions' % self._solution_limit)
			self.StopSearch()



	def solution_count(self):
		return self._solution_count
