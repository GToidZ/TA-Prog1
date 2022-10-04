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

        self.assertEqual(output.getvalue(), correct_output)
        self.assertEqual(result, 14)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=[0, 1, 15, 2])
    def test_read_dest(self, _input, output):
        result = read_dest(1)
        correct_output = "Invalid destination station index.\n" \
                         "Invalid destination station index.\n" \
                         "Invalid destination station index.\n"
        self.assertEqual(output.getvalue(), correct_output)
        self.assertEqual(result, 2)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_show_seats(self, output):
        # result = show_seats({
        #                     '1A': [{'origin': 'Bangkok', 'dest': 'Nakhon Pathom'},
        #                            {'origin': 'Ratchaburi', 'dest': 'Hua Hin'}],
        #                     '1B': [{'origin': 'Bangkok', 'dest': 'Hua Hin'}],
        #                     '1C': [{'origin': 'Bangkok', 'dest': 'Surat Thani'}],
        #                     '1D': [{'origin': 'Bangkok', 'dest': 'Hat Yai Junction'}],
        #                     '1E': [],
        #                     '1F': [],
        #                     '2A': [{'origin': 'Bang Sue Junction', 'dest': 'Phetchaburi'}],
        #                     '2B': [{'origin': 'Sala Ya', 'dest': 'Ratchaburi'},
        #                            {'origin': 'Bang Saphan Yai', 'dest': 'Thung Song Junction'}],
        #                     '2C': [{'origin': 'Sam Sen', 'dest': 'Nakhon Pathom'},
        #                            {'origin': 'Hua Hin', 'dest': 'Hat Yai Junction'}],
        #                     '2D': [{'origin': 'Ratchaburi', 'dest': 'Hat Yai Junction'}],
        #                     '2E': [{'origin': 'Phattalung', 'dest': 'Hat Yai Junction'}],
        #                     '2F': [{'origin': 'Bangkok', 'dest': 'Phetchaburi'},
        #                            {'origin': 'Hua Hin', 'dest': 'Hat Yai Junction'}],
        #                     '2G': [],
        #                     '2H': []},
        #                     station_indexes)
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
        self.assertGreaterEqual(similarily, 0.8)
        # self.assertEqual(output.getvalue(), correct_output)

    def test_get_station_index(self):
        for i in range(TOTAL_NUM_STATIONS):
            station_name = list(station_indexes.keys())[i]
            output = get_station_index(station_indexes, station_name)
            self.assertEqual(i, output)

    def test_get_station_name(self):
        for i in range(TOTAL_NUM_STATIONS):
            station_name = list(station_indexes.keys())[i]
            output = get_station_name(station_indexes, i)
            self.assertEqual(station_name, output)

    def test_check_reserved_routes(self):
        # base case
        output = check_reserved_routes({'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3, 'EE': 4},
                                       [{'origin': 'AA', 'dest': 'CC'}])
        self.assertListEqual([1, 1, 1, 0, 0], output)
        output = check_reserved_routes({'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3, 'EE': 4},
                                       [{'origin': 'AA', 'dest': 'CC'}, {'origin': 'DD', 'dest': 'EE'}])
        self.assertListEqual([1, 1, 1, 1, 1], output)
        # list value should only be max at 1
        output = check_reserved_routes({'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3, 'EE': 4},
                                       [{'origin': 'AA', 'dest': 'CC'}, {'origin': 'BB', 'dest': 'EE'}])
        self.assertListEqual([1, 1, 1, 1, 1], output)

    def test_is_ticket_available(self):
        # base case
        output = is_ticket_available([1, 1, 1, 0, 0], 3, 4)
        self.assertIs(output, True)
        output = is_ticket_available([1, 1, 1, 0, 0], 1, 2)
        self.assertIs(output, False)
        output = is_ticket_available([0, 0, 0, 1, 0, 0, 0, 0, 0], 0, 5)
        self.assertIs(output, False)

        # edge case
        output = is_ticket_available([0, 0, 0, 1, 1, 1, 0, 0, 0], 0, 2)
        self.assertIs(output, True)
        output = is_ticket_available([0, 0, 0, 1, 1, 1, 0, 0, 0], 0, 3)
        self.assertIs(output, False)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['2A', '3A', '5A', '1A'])
    def test_choose_available_seat(self, _input, output):
        available_seat = ['1A', '1B', '1C']
        result = choose_available_seat(available_seat)
        correct_output = f"Invalid seat.\n" \
                         f"Available seats: {available_seat}\n" \
                         f"Invalid seat.\n" \
                         f"Available seats: {available_seat}\n" \
                         f"Invalid seat.\n" \
                         f"Available seats: {available_seat}\n"
        similarily = SequenceMatcher(None, output.getvalue(), correct_output).ratio()
        self.assertGreaterEqual(similarily, 0.8)

    def test_update_seat(self):
        # base case
        output = update_seat({'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3, 'EE': 4}, 2, 3,
                             [{'origin': 'AA', 'dest': 'BB'}])
        self.assertListEqual([{'origin': 'AA', 'dest': 'BB'}, {'origin': 'CC', 'dest': 'DD'}], output)
        output = update_seat({'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3, 'EE': 4}, 1, 4,
                             [{'origin': 'AA', 'dest': 'DD'}])
        self.assertListEqual([{'origin': 'AA', 'dest': 'DD'}, {'origin': 'BB', 'dest': 'EE'}], output)
        output = update_seat({'AA': 0, 'BB': 1, 'CC': 2, 'DD': 3, 'EE': 4, 'FF': 5, 'GG': 6}, 1, 5,
                             [{'origin': 'AA', 'dest': 'BB'}, {'origin': 'FF', 'dest': 'GG'}])
        self.assertListEqual(
            output, [{'origin': 'AA', 'dest': 'BB'}, {'origin': 'FF', 'dest': 'GG'},
                     {'origin': 'BB', 'dest': 'FF'}])

    def test_get_ticket_price(self):
        # base case
        output = get_ticket_price({'AA': 0, 'BB': 1, 'CC': 2},
            {'AA': [0, 0], 'BB': [200, 100], 'CC': [275, 150]},
            0, 1, 2)
        self.assertEqual(output, 100)
        output = get_ticket_price({'AA': 0, 'BB': 1, 'CC': 2},
            {'AA': [0, 0], 'BB': [200, 100], 'CC': [269, 150]},
            1, 2, 1)
        self.assertEqual(output, 69)
        output = get_ticket_price({'AA': 0, 'BB': 1, 'CC': 2},
            {'AA': [0, 0], 'BB': [200, 100], 'CC': [275, 160]},
            1, 2, 2)
        self.assertEqual(output, 60)

    def test_check_available_seats(self):
        output = check_available_seats(copy.deepcopy(train_seats), station_indexes, 0, 1)
        self.assertEqual(output, ['1E', '1F', '2A', '2B', '2D', '2E', '2G', '2H'])
        output = check_available_seats(copy.deepcopy(train_seats), station_indexes, 0, 3)
        self.assertEqual(output, ['1E', '1F', '2B', '2D', '2E', '2G', '2H'])
        output = check_available_seats(copy.deepcopy(train_seats), station_indexes, 0, 6)
        self.assertEqual(output, ['1E', '1F', '2E', '2G', '2H'])
        output = check_available_seats(copy.deepcopy(train_seats), station_indexes, 0, 14)
        self.assertEqual(output, ['1E', '1F', '2G', '2H'])

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
        self.assertGreaterEqual(similarily, 0.8)
        self.assertIs(val_returned, None)
        correct_train_seats = copy.deepcopy(train_seats)
        correct_train_seats['1B'].append({'origin': 'Chumphon', 'dest': 'Phattalung'})
        self.assertDictEqual(demo_train_seats, correct_train_seats)

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
        similarily = SequenceMatcher(None, output.getvalue(), correct_output).ratio()
        self.assertGreaterEqual(similarily, 0.9)
        self.assertEqual(result, '2A')

    def test_remove_ticket(self):
        # seat_str exist
        demo_train_seats = copy.deepcopy(train_seats)
        output = remove_ticket(demo_train_seats, station_indexes, '1A', 0, 1)
        self.assertIs(output, False)
        self.assertDictEqual(demo_train_seats, train_seats)
        output = remove_ticket(demo_train_seats, station_indexes, '1A', 0, 4)
        self.assertIs(output, False)
        self.assertDictEqual(demo_train_seats, train_seats)
        output = remove_ticket(demo_train_seats, station_indexes, '2B', 4, 5)
        self.assertIs(output, False)
        self.assertDictEqual(demo_train_seats, train_seats)
        output = remove_ticket(demo_train_seats, station_indexes, '2B', 0, 1)
        self.assertIs(output, False)
        self.assertDictEqual(demo_train_seats, train_seats)
        output = remove_ticket(demo_train_seats, station_indexes, '1A', 0, 5)
        self.assertIs(output, True)
        correct_output = copy.deepcopy(train_seats)
        correct_output['1A'].pop(0)
        self.assertDictEqual(demo_train_seats, correct_output)

    def test_cancel(self):
        pass

    def test_show_ticket_prices(self):
        pass

    def clear_tickets(self):
        pass

# station_fees, station_indexes = read_stations('south_stations.txt')
# print(station_fees)        # you can uncomment this line to see output
# print(station_indexes)     # you can uncomment this line to see output
# TOTAL_NUM_STATIONS = len(station_indexes)
# #print(TOTAL_NUM_STATIONS)  # you can uncomment this line to see output
#
# train_seats, train_seat_classes = read_seats('south_train_seats.txt')
# # print(train_seats)         # you can uncomment this line to see output
# # print(train_seat_classes)  # you can uncomment this line to see output
#
# read_reserved_tickets('south_reserved_tickets.txt', train_seats)
# #print(train_seats)        # you can uncomment this line to see output
#
# station = list(station_indexes.values())[0]
#
# print(station)