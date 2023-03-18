import unittest
from models.instructor import Instructor
from tests.factory.instructor_factory import InstructorFactory

class TestInstructor(unittest.TestCase):

    def setUp(self):
        self.instructor = InstructorFactory.create_instructor()

    def test_initially_students_list_is_empty(self):
        self.assertEqual(len(self.instructor.students), 0)

    def test_add_student(self):
        self.instructor.add_student('fake_student')
        self.assertIn('fake_student', self.instructor.students)

if __name__ == '__main__':
    unittest.main()
