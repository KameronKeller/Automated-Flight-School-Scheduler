from ortools.sat.python import cp_model

model = cp_model.CpModel()

days = ['monday', 'tuesday', 'wednesday']
students = ['tommy', 'sue', 'joe']
aircraft = ['r22-1']
hourly_blocks = [8]

blocks = {}

for d in days:
	for s in students:
		for a in aircraft:
			for b in hourly_blocks:
				blocks[(d, s, a, b)] = model.NewBoolVar('block %s %s %s %i' % (d, s, a, b))

# Each student must have exactly 3 flights per week
for student in students:
	model.Add(sum(blocks[(day, student, aircraft_type, block)] for day in days for aircraft_type in aircraft for block in hourly_blocks) == 3)

# Each flight must be on a different day
for d in days:
	for s in students:
		model.Add(sum(blocks[(d, s, a, b)] for a in aircraft for b in hourly_blocks) <= 1)
# model.Add(sum(blocks[(d, s, a, b)] for a in aircraft for b in hourly_blocks) <= 1)

# for d in days:
# 	for a in aircraft:
# 		for b in blocks:
# 			print((blocks[(d, s, a, b)] for s in students))
# 			model.AddExactlyOne(blocks[(d, s, a, b)] for s in students)


solver = cp_model.CpSolver()
status = solver.Solve(model)

# This works, but I think solution callback is a better solution
# if status == cp_model.OPTIMAL:
# 	for d in days:
# 		for s in students:
# 			for a in aircraft:
# 				for b in hourly_blocks:
# 					# print(solver.BooleanValue(blocks[(d, s, a, b)]))
# 					if solver.BooleanValue(blocks[(d, s, a, b)]) == True:
# 						print(f'{d}: {s} flies {a} at {b} hour')
# else:
# 	print('No solution found.')


class SolutionPrinter(cp_model.CpSolverSolutionCallback):

	def __init__(self, blocks, days, students, aircraft, hourly_blocks, limit):
		cp_model.CpSolverSolutionCallback.__init__(self)
		self._blocks = blocks
		self._days = days
		self._students = students
		self._aircraft = aircraft
		self._hourly_blocks = hourly_blocks
		self._solution_count = 0
		self._solution_limit = limit

	def on_solution_callback(self):
		self._solution_count += 1
		print('Solution %i' % self._solution_count)
		for d in self._days:
			print('%s' % d)
			for s in self._students:
				for a in self._aircraft:
					if self.Value(self._blocks[(d, s, a, b)]):
						print(f'{s} flies {a} at {b} hour')
		if self._solution_count >= self._solution_limit:
			print('Stop search after %i solutions' % self._solution_limit)
			self.StopSearch()

	def solution_count(self):
		return self._solution_count

solution_limit = 5
solution_printer = SolutionPrinter(blocks, days, students, aircraft, hourly_blocks, solution_limit)
solver.Solve(model, solution_printer)

# Statistics.
print('\nStatistics')
print('  - conflicts      : %i' % solver.NumConflicts())
print('  - branches       : %i' % solver.NumBranches())
print('  - wall time      : %f s' % solver.WallTime())
print('  - solutions found: %i' % solution_printer.solution_count())


# # print(status)

# # print(solver.SolutionInfo())
# # print(solver.ResponseStats())


# for d in days:
# 	for s in students:
# 		for a in aircraft:
# 			for b in blocks:
# 				print(blocks[(d, s, a, b)])
# # print(solver.Value())



  # # Retrieve the solution
  # for i in instructors:
  #   for j in students:
  #     for k in aircrafts:
  #       for l in slots:
  #         if solver.Value(flight[(i, j, k, l)]) == 1:
  #           print(f'{i} is scheduled with {j} on {k} at {l}')
