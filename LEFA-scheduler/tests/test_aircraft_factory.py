import unittest
from models.aircraft_factory import AircraftFactory

class TestAircraftFactory(unittest.TestCase):

    # def test_attributes(self):

    def setUp(self):
        self.aircraft_factory = AircraftFactory()

    def test_calculate_blocks_odd_to_odd(self):
        first_block = 7
        last_block = 17
        schedule_blocks = self.aircraft_factory.calculate_blocks(first_block, last_block)
        self.assertEqual(schedule_blocks, [7, 9, 11, 13, 15, 17])

    def test_build_aircraft_of_model_creates_n_aicraft(self):
        n = 6
        aircraft = self.aircraft_factory.build_aircraft_of_model(
                                        name_prefix = 'R22',
                                        model = 'R22',
                                        num_aircraft = n,
                                        earliest_block = 7,
                                        latest_block = 17)
        self.assertEqual(n, len(aircraft))

    def test_if_earliest_block_is_odd_then_more_odd_aircraft_are_created(self):
        odd_count = 0
        even_count = 0
        n = 5
        aircraft = self.aircraft_factory.build_aircraft_of_model(
                                            name_prefix = 'R22',
                                            model = 'R22',
                                            num_aircraft = n,
                                            earliest_block = 7,
                                            latest_block = 17)
        for a in aircraft.values():
            if a.block_type == 'odd':
                odd_count += 1
            elif a.block_type == 'even':
                even_count += 1

        self.assertEqual(odd_count, 3)
        self.assertEqual(even_count, 2)






if __name__ == '__main__':
    unittest.main()
