import unittest
from models.person import Person
from tests.factory.person_factory import PersonFactory

class TestPerson(unittest.TestCase):

    def setUp(self):
        self.person = PersonFactory.create_person()

    def test_attributes(self):
        self.assertEqual('first', self.person.first_name)
        self.assertEqual('last', self.person.last_name)

    def test_parse_unavailability(self):
        provided_unavailability = {
            'fixedwing_friday_unavailability': '05:30;06:30;',
            'fixedwing_monday_unavailability': '06:30;05:30;09:30;11:30;10:30;',
            'fixedwing_saturday_unavailability': '05:30;06:30;07:30;08:30;09:30;10:30;11:30;12:30;13:30;14:30;15:30;16:30;17:30;18:30;19:30;20:30;',
            'fixedwing_sunday_unavailability': '05:30;06:30;07:30;08:30;09:30;10:30;11:30;12:30;13:30;14:30;15:30;16:30;17:30;18:30;19:30;20:30;',
            'fixedwing_thursday_unavailability': '05:30;06:30;',
            'fixedwing_tuesday_unavailability': '06:30;05:30;',
            'fixedwing_wednesday_unavailability': '05:30;06:30;'}

        expected_unavailability = {
            'fixedwing_friday_unavailability': {5, 6},
            'fixedwing_monday_unavailability': {5, 6, 9, 10, 11},
            'fixedwing_saturday_unavailability': {5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20},
            'fixedwing_sunday_unavailability': {5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20},
            'fixedwing_thursday_unavailability': {5, 6},
            'fixedwing_tuesday_unavailability': {5, 6},
            'fixedwing_wednesday_unavailability': {5, 6}}

        unavailability = self.person.parse_unavailability(provided_unavailability)

        self.assertEqual(expected_unavailability, unavailability)


if __name__ == '__main__':
    unittest.main()
