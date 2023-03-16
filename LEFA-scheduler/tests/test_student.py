import unittest
from models.student import Student

class TestStudent(unittest.TestCase):

    def setUp(self):
        self.student = Student('first', 'last', 'unavailable', 'rating', 'instructor')

    def test_attributes(self):
        self.assertEqual(self.student.rating, 'rating')
        self.assertEqual(self.student.instructor, 'instructor')

if __name__ == '__main__':
    unittest.main()
