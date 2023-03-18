import unittest
from models.instructor_student import InstructorStudent

class TestInstructorStudent(unittest.TestCase):

    def setUp(self):
        self.instructor_student = InstructorStudent('first', 'last', 'unavailable', 'rating', 'schedule_type', 'instructor', ['student_1'])

    def test_attributes(self):
        self.assertEqual(self.instructor_student.first_name, 'first')
        self.assertEqual(self.instructor_student.last_name, 'last')
        self.assertEqual(self.instructor_student.unavailability, 'unavailable')
        self.assertEqual(self.instructor_student.rating, 'rating')
        self.assertEqual(self.instructor_student.schedule_type, 'schedule_type')
        self.assertEqual(self.instructor_student.instructor, 'instructor')

if __name__ == '__main__':
    unittest.main()
