import unittest
from models.person import Person

class TestPerson(unittest.TestCase):

    def test_attributes(self):
        person = Person('first', 'last', 'unavailable')
        self.assertEqual('first', person.first_name)
        self.assertEqual('last', person.last_name)
        self.assertEqual('unavailable', person.unavailability)

if __name__ == '__main__':
    unittest.main()
