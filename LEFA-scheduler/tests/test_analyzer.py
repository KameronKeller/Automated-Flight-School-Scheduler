from models.analyzer import Analyzer
from models.instructor import Instructor

class TestAnalyzer(unittest.TestCase):

	def setUp(self):
		self.calendar = Calendar(earliest_block=7, latest_block=17)
		self.instructors = {}
		self.instructor = InstructorFactory.create_free_instructor()
		self.s1 = StudentFactory.create_free_student(first_name='s1', rating='Commercial', schedule_type='Fixed-Wing')
		self.s2 = StudentFactory.create_free_student(first_name='s2', rating='Instrument', schedule_type='Rotor-Wing')
		self.instructor.add_student(s1)
		self.instructor.add_student(s2)
		self.instructors[self.instructor.full_name] = self.instructor
		self.analyzer = Analyzer(self.instructors, self.calendar)




if __name__ == '__main__':
    unittest.main()
