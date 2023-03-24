import csv

class CsvParser:

	def __init__(self, csv_path):
		self.csv_path = csv_path

	

	def get_names(self):
		with open(self.csv_path) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			line_count = 0
			for row in csv_reader:
				if line_count == 0:
					print(f'Column names are {", ".join(row)}')
					line_count += 1
				# else:
				# 	print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
				# 	line_count += 1
			print(f'Processed {line_count} lines.')

	def parse_unavailability(self, unavailability):
		parsed_unavailability = {}
		for day, times in unavailability.items():
			parsed_unavailability[day] = times.split(';')

		return parsed_unavailability
