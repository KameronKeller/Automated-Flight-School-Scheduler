import unittest
from models.student import Student
from tests.factory.student_factory import StudentFactory

class TestStudent(unittest.TestCase):

    def setUp(self):
        self.student = StudentFactory.create_student()

    def test_attributes(self):
        self.assertEqual(self.student.rating, 'rating')
        self.assertEqual(self.student.instructor, 'instructor')
        self.assertEqual(self.student.first_name, 'first')
        self.assertEqual(self.student.last_name, 'last')
        self.assertEqual(self.student.schedule_type, 'schedule_type')

    def test_Private_Rotor_Wing_aircraft_requirements(self):
        expected_aircraft = 'R22'
        expected_dual_frequency = {'dual' : 3}
        student = StudentFactory.create_student()
        student.rating = 'Private'
        student.schedule_type = 'Rotor-Wing'
        student.aircraft = student.determine_aircraft(student.rating, student.schedule_type)
        self.assertEqual(len(student.aircraft), 1)
        self.assertIn(expected_aircraft, student.aircraft)
        self.assertEqual(student.aircraft['R22'], expected_dual_frequency)

    # def test_Instrument_Rotor_Wing_aircraft_requirements(self):


    # def test_Commercial_Rotor_Wing_aircraft_requirements(self):


    # def test_CFI_Rotor_Wing_aircraft_requirements(self):


    # def test_CFII_Rotor_Wing_aircraft_requirements(self):


    # def test_Private_Fixed_Wing_aircraft_requirements(self):


    # def test_Instrument_Fixed_Wing_aircraft_requirements(self):


    # def test_Commercial_Fixed_Wing_aircraft_requirements(self):


    # def test_CFI_Fixed_Wing_aircraft_requirements(self):


    # def test_CFII_Fixed_Wing_aircraft_requirements(self):


    # def test_MEI_Fixed_Wing_aircraft_requirements(self):



if __name__ == '__main__':
    unittest.main()
