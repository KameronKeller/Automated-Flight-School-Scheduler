from ortools.sat.python import cp_model

print("====================")

model = cp_model.CpModel()

# days = ['monday']
days = ['monday', 'tuesday', 'wednesday']
students = ['tommy', 'sue', 'joe']
# students = ['tommy']
# students = ['tommy', 'sue']
# aircraft = ['a1']
aircraft = ['a1', 'a2', 'a3', 'a4', 'a5']
hourly_blocks = ['8', '9', '10']
# hourly_blocks = ['8']

schedule = {}

for d in days:
	for s in students:
		for a in aircraft:
			for b in hourly_blocks:
				schedule[(d, s, a, b)] = model.NewBoolVar('block %s %s %s %s' % (d, s, a, b))




# # Students can only have one flight per day
# for d in days:
# 	for s in students:
# 		model.AddAtMostOne(schedule[(d, s, a, b)] for a in aircraft for b in hourly_blocks)
# 		# model.Add(sum(schedule[(d, s, a, b)] for a in aircraft for b in hourly_blocks) <= 1)


# # Only one student can occupy an aircraft at a given time
# for d in days:
# 	for a in aircraft:
# 		for b in hourly_blocks:
# 			model.AddAtMostOne(schedule[(d, s, a, b)] for s in students)



# Each student must have exactly 3 flights per week
for student in students:
	model.Add(sum(schedule[(day, student, aircraft_type, block)] for day in days for aircraft_type in aircraft for block in hourly_blocks) == 3)

# Each flight must be on a different day
for d in days:
	for s in students:
		# model.Add(sum(schedule[(d, s, a, b)] for a in aircraft for b in hourly_blocks) <= 1)
		model.AddAtMostOne(schedule[(d, s, a, b)] for a in aircraft for b in hourly_blocks)

# Each aircraft can only hold one person per hourly block, per day
for a in aircraft:
	for d in days:
		for b in hourly_blocks:
			model.AddAtMostOne(schedule[(d, s, a, b)] for s in students)
# # 			model.Add(sum(schedule[(d, s, a, b)] for s in students for d in days) == len(students))


solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0
# Enumerate all solutions.
solver.parameters.enumerate_all_solutions = True



class SolutionPrinter(cp_model.CpSolverSolutionCallback):

	def __init__(self, schedule, days, students, aircraft, hourly_blocks, limit):
		cp_model.CpSolverSolutionCallback.__init__(self)
		self._blocks = schedule
		self._days = days
		self._students = students
		self._aircraft = aircraft
		self._hourly_blocks = hourly_blocks
		self._solution_count = 0
		self._solution_limit = limit

	def on_solution_callback(self):
		self._solution_count += 1
		print('\nSolution %i' % self._solution_count)
		for d in self._days:
			print('%s' % d)
			for s in self._students:
				for a in self._aircraft:
					for b in self._hourly_blocks:
						if self.Value(self._blocks[(d, s, a, b)]):
							print(f'{s} flies {a} at {b}')
		if self._solution_count >= self._solution_limit:
			print('Stop search after %i solutions' % self._solution_limit)
			self.StopSearch()

	def solution_count(self):
		return self._solution_count

solution_limit = 5
solution_printer = SolutionPrinter(schedule, days, students, aircraft, hourly_blocks, solution_limit)
status = solver.Solve(model, solution_printer)

# Statistics.
print('\nStatistics')
print('  - status         : {}'.format(status))
print('  - conflicts      : %i' % solver.NumConflicts())
print('  - branches       : %i' % solver.NumBranches())
print('  - wall time      : %f s' % solver.WallTime())
print('  - solutions found: %i' % solution_printer.solution_count())

# print(cp_model.OPTIMAL)
# print(cp_model.FEASIBLE)
# print(cp_model.INFEASIBLE)
# print(cp_model.MODEL_INVALID)
# print(cp_model.UNKNOWN)


# This works, but I think solution callback is a better solution
# if status == cp_model.OPTIMAL:
# 	for d in days:
# 		for s in students:
# 			for a in aircraft:
# 				for b in hourly_blocks:
# 					# print(solver.BooleanValue(schedule[(d, s, a, b)]))
# 					if solver.BooleanValue(schedule[(d, s, a, b)]) == True:
# 						print(f'{d}: {s} flies {a} at {b} hour')
# else:
# 	print('No solution found.')

