import unittest
from models.schedule_builder import ScheduleBuilder
from models.instructor import Instructor

class TestScheduleBuilder(unittest.TestCase):

    def setUp(self):
        self.instructor = Instructor('first', 'last', 'unavailable')
        # self.aircraft = Aircraft()
        self.schedule_builder = ScheduleBuilder([self.instructor])

    def test_attributes(self):
        self.assertEqual(self.schedule_builder.instructors, [self.instructor])

if __name__ == '__main__':
    unittest.main()
