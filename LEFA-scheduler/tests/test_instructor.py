import unittest
from models.instructor import Instructor

class TestInstructor(unittest.TestCase):

    def setUp(self):
        self.instructor = Instructor('first', 'last', 'unavailable')

    def test_attributes(self):
        self.assertEqual(len(self.instructor.students), 0)

    def test_add_student(self):
        self.instructor.add_student('fake_student')
        self.assertIn('fake_student', self.instructor.students)

if __name__ == '__main__':
    unittest.main()
