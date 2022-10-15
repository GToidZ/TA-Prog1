import io
import copy
from manage_train import *
from unittest.mock import patch
import unittest
from difflib import SequenceMatcher


class TestManageTrain(unittest.TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=[-1, 15, 14])
    def test_read_origin(self, _input, output):
        result = read_origin()
        correct_output = f"Invalid origin station index.\n" \
                         f"Invalid origin station index.\n"

        self.assertEqual(output.getvalue(), correct_output, 'Display outputs are not equal')
        self.assertEqual(result, 14, 'Return value is not equal')

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=[0, 1, 15, 2])
    def test_read_dest(self, _input, output):
        result = read_dest(1)
        correct_output = "Invalid destination station index.\n" \
                         "Invalid destination station index.\n" \
                         "Invalid destination station index.\n"
        self.assertEqual(output.getvalue(), correct_output, 'Display outputs are not equal')
        self.assertEqual(result, 2, 'Return value is not equal')

    def test_get_station_index(self):
        for i in range(TOTAL_NUM_STATIONS):
            station_name = list(station_indexes.keys())[i]
            output = get_station_index(station_indexes, station_name)
            self.assertEqual(i, output, f'Return value {i+1} is not equal')

    def test_get_station_name(self):
        for i in range(TOTAL_NUM_STATIONS):
            station_name = list(station_indexes.keys())[i]
            output = get_station_name(station_indexes, i)
            self.assertEqual(station_name, output, f'Return value {i+1} is not equal')

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_show_seats(self, output):
        result = show_seats(copy.deepcopy(train_seats), station_indexes)
        correct_output = "1A: [Bangkok(0)-Nakhon Pathom(5)], [Ratchaburi(6)-Hua Hin(8)],\n" \
                         "1B: [Bangkok(0)-Hua Hin(8)],\n" \
                         "1C: [Bangkok(0)-Surat Thani(11)],\n" \
                         "1D: [Bangkok(0)-Hat Yai Junction(14)],\n" \
                         "1E: \n" \
                         "1F: \n" \
                         "2A: [Bang Sue Junction(2)-Phetchaburi(7)],\n" \
                         "2B: [Sala Ya(4)-Ratchaburi(6)], [Bang Saphan Yai(9)-Thung Song Junction(12)],\n" \
                         "2C: [Sam Sen(1)-Nakhon Pathom(5)], [Hua Hin(8)-Hat Yai Junction(14)],\n" \
                         "2D: [Ratchaburi(6)-Hat Yai Junction(14)],\n" \
                         "2E: [Phattalung(13)-Hat Yai Junction(14)],\n" \
                         "2F: [Bangkok(0)-Phetchaburi(7)], [Hua Hin(8)-Hat Yai Junction(14)],\n" \
                         "2G: \n" \
                         "2H: \n"
        similarily = SequenceMatcher(None, output.getvalue(), correct_output).ratio()
        self.assertGreaterEqual(similarily, 0.8, 'Percentage of correctness belows 0.8')

    def test_check_reserved_routes(self):
        # base case
        output = check_reserved_routes({'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3, 'EE': 4},
                                       [{'origin': 'AA', 'dest': 'CC'}])
        self.assertListEqual([1, 1, 1, 0, 0], output, 'Return list is not equal')
        output = check_reserved_routes({'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3, 'EE': 4},
                                       [{'origin': 'AA', 'dest': 'CC'}, {'origin': 'DD', 'dest': 'EE'}])
        self.assertListEqual([1, 1, 1, 1, 1], output, 'Return list is not equal')
        # list value should only be max at 1
        output = check_reserved_routes({'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3, 'EE': 4},
                                       [{'origin': 'AA', 'dest': 'CC'}, {'origin': 'BB', 'dest': 'EE'}])
        self.assertListEqual([1, 1, 1, 1, 1], output, 'Return list is not equal')

    def test_is_ticket_available(self):
        # base case
        output = is_ticket_available([1, 1, 1, 0, 0], 3, 4)
        self.assertIs(output, True, 'Return value supposed to be True')
        output = is_ticket_available([1, 1, 1, 0, 0], 1, 2)
        self.assertIs(output, False, 'Return value supposed to be False')
        output = is_ticket_available([0, 0, 0, 1, 0, 0, 0, 0, 0], 0, 5)
        self.assertIs(output, False, 'Return value supposed to be False')

        # edge case
        output = is_ticket_available([0, 0, 0, 1, 1, 1, 0, 0, 0], 0, 2)
        self.assertIs(output, True, 'Return value supposed to be True')
        output = is_ticket_available([0, 0, 0, 1, 1, 1, 0, 0, 0], 0, 3)
        self.assertIs(output, False, 'Return value supposed to be False')

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['2A', '3A', '5A', '1A'])
    def test_choose_available_seat(self, _input, output):
        available_seat = ['1A', '1B', '1C']
        choose_available_seat(available_seat)
        correct_output = f"Invalid seat.\n" \
                         f"Available seats: {available_seat}\n" \
                         f"Invalid seat.\n" \
                         f"Available seats: {available_seat}\n" \
                         f"Invalid seat.\n" \
                         f"Available seats: {available_seat}\n"
        correct_output2 = f"Invalid seat.\n" \
                          f"Invalid seat.\n" \
                          f"Invalid seat.\n" \

        similarity = SequenceMatcher(None, output.getvalue(), correct_output).ratio()
        similarity2 = SequenceMatcher(None, output.getvalue(), correct_output2).ratio()
        is_pass = (similarity >= 0.8) or (similarity2 >= 0.8)
        self.assertTrue(is_pass, 'Percentage of correctness belows 0.8')

    def test_update_seat(self):
        # base case
        output = update_seat({'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3, 'EE': 4}, 2, 3,
                             [{'origin': 'AA', 'dest': 'BB'}])
        self.assertListEqual([{'origin': 'AA', 'dest': 'BB'}, {'origin': 'CC', 'dest': 'DD'}], output,
                             'Return List are not equal')
        output = update_seat({'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3, 'EE': 4}, 1, 4,
                             [{'origin': 'AA', 'dest': 'DD'}])
        self.assertListEqual([{'origin': 'AA', 'dest': 'DD'}, {'origin': 'BB', 'dest': 'EE'}], output,
                             'Return List are not equal')
        output = update_seat({'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3, 'EE': 4, 'FF': 5, 'GG': 6}, 1, 5,
                             [{'origin': 'AA', 'dest': 'BB'}, {'origin': 'FF', 'dest': 'GG'}])
        self.assertListEqual(
            output, [{'origin': 'AA', 'dest': 'BB'}, {'origin': 'FF', 'dest': 'GG'},
                     {'origin': 'BB', 'dest': 'FF'}], 'Return List are not equal')

    def test_get_ticket_price(self):
        # base case
        output = get_ticket_price({'AA': 0, 'BB': 1, 'CC': 2},
                                  {'AA': [0, 0], 'BB': [200, 100], 'CC': [275, 150]},
                                  0, 1, 2)
        self.assertEqual(output, 100, 'Return value is not equal')
        output = get_ticket_price({'AA': 0, 'BB': 1, 'CC': 2},
                                  {'AA': [0, 0], 'BB': [200, 100], 'CC': [269, 150]},
                                  1, 2, 1)
        self.assertEqual(output, 69, 'Return value is not equal')
        output = get_ticket_price({'AA': 0, 'BB': 1, 'CC': 2},
                                  {'AA': [0, 0], 'BB': [200, 100], 'CC': [275, 160]},
                                  1, 2, 2)
        self.assertEqual(output, 60, 'Return value is not equal')

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=[10, -1, 15, 9, 13, '1B'])
    def test_reserve(self, _input, output):
        demo_train_seats = copy.deepcopy(train_seats)
        val_returned = reserve(demo_train_seats, train_seat_classes, station_indexes, station_fees)
        correct_output = "Invalid destination station index.\n" \
                         "Invalid destination station index.\n" \
                         "Invalid destination station index.\n" \
                         "Available seats: ['1A', '1B', '1E', '1F', '2A', '2G', '2H']\n" \
                         "Class 1 Ticket price = 300\n" \
                         "Class 2 Ticket price = 180\n" \
                         "The selected seat = 1B\n" \
                         "The ticket price = 300\n"
        similarily = SequenceMatcher(None, output.getvalue(), correct_output).ratio()
        self.assertGreaterEqual(similarily, 0.8, 'Percentage of correctness belows 0.8')
        self.assertIs(val_returned, None, 'Return value should be None')
        correct_train_seats = copy.deepcopy(train_seats)
        correct_train_seats['1B'].append({'origin': 'Chumphon', 'dest': 'Phattalung'})
        self.assertDictEqual(demo_train_seats, correct_train_seats, 'train_seats content unmatched')

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['1AA', '2I', '1', 'A', '1a', '2b', '2A'])
    def test_read_canceled_seat(self, _input, output):
        result = read_canceled_seat(copy.deepcopy(train_seats))
        correct_output = "Seats are ['1A', '1B', '1C', '1D', '1E', '1F', '2A', '2B', '2C', '2D', '2E', '2F', '2G', '2H']\n" \
                         "Invalid seat.\n" \
                         "Invalid seat.\n" \
                         "Invalid seat.\n" \
                         "Invalid seat.\n" \
                         "Invalid seat.\n" \
                         "Invalid seat.\n"
        correct_output2 = "Invalid seat.\n" \
                          "Invalid seat.\n" \
                          "Invalid seat.\n" \
                          "Invalid seat.\n" \
                          "Invalid seat.\n" \
                          "Invalid seat.\n"
        similarity = SequenceMatcher(None, output.getvalue(), correct_output).ratio()
        similarity2 = SequenceMatcher(None, output.getvalue(), correct_output2).ratio()
        is_pass = (similarity >= 0.9) or (similarity2 >= 0.9)
        self.assertTrue(is_pass, 'Percentage of correctness belows 0.9')
        self.assertEqual(result, '2A', 'Return value is not equal')

    def test_remove_ticket(self):
        # seat_str exist
        demo_train_seats = copy.deepcopy(train_seats)
        output = remove_ticket(demo_train_seats, station_indexes, '1A', 0, 1)
        self.assertIs(output, False, 'Return value supposed to be False')
        self.assertDictEqual(demo_train_seats, train_seats)
        output = remove_ticket(demo_train_seats, station_indexes, '1A', 0, 4)
        self.assertIs(output, False, 'Return value supposed to be False')
        self.assertDictEqual(demo_train_seats, train_seats)
        output = remove_ticket(demo_train_seats, station_indexes, '2B', 4, 5)
        self.assertIs(output, False, 'Return value supposed to be False')
        self.assertDictEqual(demo_train_seats, train_seats)
        output = remove_ticket(demo_train_seats, station_indexes, '2B', 0, 1)
        self.assertIs(output, False, 'Return value supposed to be False')
        self.assertDictEqual(demo_train_seats, train_seats)
        output = remove_ticket(demo_train_seats, station_indexes, '1A', 0, 5)
        self.assertIs(output, True, 'Return value supposed to be True')
        correct_output = copy.deepcopy(train_seats)
        correct_output['1A'].pop(0)
        self.assertDictEqual(demo_train_seats, correct_output, 'train_seats content unmatched')

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['1G', '1E', 2, 13])
    def test_cancel1(self, _input, output):
        demo_train_seats = copy.deepcopy(train_seats)
        correct_train_seats = copy.deepcopy(train_seats)
        val_returned = cancel(demo_train_seats, station_indexes)
        correct_output = "Seats are ['1A', '1B', '1C', '1D', '1E', '1F', '2A', '2B', '2C', '2D', '2E', '2F', '2G','2H']\n" \
                         "Invalid seat.\n" \
                         "Tickets issued at 1E: \n" \
                         "Ticket does not exist at 1E\n"
        similarily = SequenceMatcher(None, output.getvalue(), correct_output).ratio()
        self.assertGreaterEqual(similarily, 0.8, 'Percentage of correctness belows 0.8')
        self.assertIs(val_returned, None, 'Return value should be None')
        self.assertDictEqual(demo_train_seats, correct_train_seats, 'train_seats content unmatched')

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['2B', 4, 6])
    def test_cancel2(self, _input, output):
        demo_train_seats = copy.deepcopy(train_seats)
        correct_train_seats = copy.deepcopy(train_seats)
        val_returned = cancel(demo_train_seats, station_indexes)
        correct_output = "Seats are ['1A', '1B', '1C', '1D', '1E', '1F', '2A', '2B', '2C', '2D', '2E', '2F', '2G','2H']\n" \
                         "Tickets issued at 2B: [Sala Ya(4)-Ratchaburi(6)], [Bang Saphan Yai(9)-Thung Song Junction(12)], \n" \
                         "After cancellation: \n" \
                         "Tickets issued at 2B: [Bang Saphan Yai(9)-Thung Song Junction(12)], \n"
        similarily = SequenceMatcher(None, output.getvalue(), correct_output).ratio()
        self.assertGreaterEqual(similarily, 0.8, 'Percentage of correctness belows 0.8')
        self.assertIs(val_returned, None, 'Return value should be None')
        correct_train_seats['2B'].pop(0)
        self.assertDictEqual(demo_train_seats, correct_train_seats, 'train_seats content unmatched')

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_show_ticket_prices(self, output):
        demo_train_seats = copy.deepcopy(train_seats)
        show_ticket_prices(demo_train_seats, station_indexes, station_fees)
        correct_output = "1A: [Bangkok(0)-Nakhon Pathom(5)-860], [Ratchaburi(6)-Hua Hin(8)-100], \n" \
                         "1B: [Bangkok(0)-Hua Hin(8)-1000], \n" \
                         "1C: [Bangkok(0)-Surat Thani(11)-1300], \n" \
                         "1D: [Bangkok(0)-Hat Yai Junction(14)-1600], \n" \
                         "1E: \n" \
                         "1F: \n" \
                         "2A: [Bang Sue Junction(2)-Phetchaburi(7)-80], \n" \
                         "2B: [Sala Ya(4)-Ratchaburi(6)-30], [Bang Saphan Yai(9)-Thung Song Junction(12)-170], \n" \
                         "2C: [Sam Sen(1)-Nakhon Pathom(5)-30], [Hua Hin(8)-Hat Yai Junction(14)-300], \n" \
                         "2D: [Ratchaburi(6)-Hat Yai Junction(14)-350], \n" \
                         "2E: [Phattalung(13)-Hat Yai Junction(14)-20], \n" \
                         "2F: [Bangkok(0)-Phetchaburi(7)-680], [Hua Hin(8)-Hat Yai Junction(14)-300], \n" \
                         "2G: \n" \
                         "2H: \n"
        similarily = SequenceMatcher(None, output.getvalue(), correct_output).ratio()
        self.assertGreaterEqual(similarily, 0.8, 'Percentage of correctness belows 0.8')

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_clear_tickets(self, output):
        demo_train_seats = copy.deepcopy(train_seats)
        correct_train_seats = copy.deepcopy(train_seats)
        clear_tickets(train_seats=demo_train_seats)
        for seat_id in correct_train_seats.keys():
            correct_train_seats[seat_id] = []
        self.assertDictEqual(demo_train_seats, correct_train_seats, 'train_seats content unmatched')


if __name__ == '__main__':
    unittest.main()
