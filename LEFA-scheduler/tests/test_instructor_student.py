import unittest
from models.instructor_student import InstructorStudent
from tests.factory.instructor_student_factory import InstructorStudentFactory

class TestInstructorStudent(unittest.TestCase):

    def setUp(self):
        self.instructor_student = InstructorStudentFactory.create_instructor_student()

    def test_attributes(self):
        self.assertEqual(self.instructor_student.first_name, 'first')
        self.assertEqual(self.instructor_student.last_name, 'last')
        self.assertEqual(self.instructor_student.rating, 'rating')
        self.assertEqual(self.instructor_student.schedule_type, 'schedule_type')
        self.assertEqual(self.instructor_student.instructor, 'instructor')

if __name__ == '__main__':
    unittest.main()
