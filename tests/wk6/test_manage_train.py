from manage_train import *

import unittest


class TestManageTrain(unittest.TestCase):

    def setUp(self):
        # self.station_fees, self.station_indexes = read_stations('south_stations.txt')
        # self.TOTAL_NUM_STATIONS = len(station_indexes)
        # self.train_seats, self.train_seat_classes = read_seats('south_train_seats.txt')
        # read_reserved_tickets('south_reserved_tickets.txt', self.train_seats)

        self.station_fees = {'Bangkok': [0, 0], 'Sam Sen': [800, 600], 'Bang Sue Junction': [800, 600],
                             'Bang Bamru': [820, 610], 'Sala Ya': [830, 620], 'Nakhon Pathom': [860, 630],
                             'Ratchaburi': [900, 650], 'Phetchaburi': [950, 680], 'Hua Hin': [1000, 700],
                             'Bang Saphan Yai': [1100, 780], 'Chumphon': [1200, 800], 'Surat Thani': [1300, 900],
                             'Thung Song Junction': [1400, 950], 'Phattalung': [1500, 980],'Hat Yai Junction': [1600, 1000]}

        self.station_indexes = {'Bangkok': 0, 'Sam Sen': 1, 'Bang Sue Junction': 2, 'Bang Bamru': 3,
                                'Sala Ya': 4, 'Nakhon Pathom': 5, 'Ratchaburi': 6, 'Phetchaburi': 7,
                                'Hua Hin': 8, 'Bang Saphan Yai': 9, 'Chumphon': 10, 'Surat Thani': 11,
                                'Thung Song Junction': 12, 'Phattalung': 13, 'Hat Yai Junction': 14}

        self.TOTAL_NUM_STATIONS = len(self.station_indexes)

        self.train_seats = {'1A': [{'origin': 'Bangkok', 'dest': 'Nakhon Pathom'},
                                   {'origin': 'Ratchaburi', 'dest': 'Hua Hin'}],
                            '1B': [{'origin': 'Bangkok', 'dest': 'Hua Hin'}],
                            '1C': [{'origin': 'Bangkok', 'dest': 'Surat Thani'}],
                            '1D': [{'origin': 'Bangkok', 'dest': 'Hat Yai Junction'}],
                            '1E': [],
                            '1F': [],
                            '2A': [{'origin': 'Bang Sue Junction', 'dest': 'Phetchaburi'}],
                            '2B': [{'origin': 'Sala Ya', 'dest': 'Ratchaburi'},
                                   {'origin': 'Bang Saphan Yai', 'dest': 'Thung Song Junction'}],
                            '2C': [{'origin': 'Sam Sen', 'dest': 'Nakhon Pathom'},
                                   {'origin': 'Hua Hin', 'dest': 'Hat Yai Junction'}],
                            '2D': [{'origin': 'Ratchaburi', 'dest': 'Hat Yai Junction'}],
                            '2E': [{'origin': 'Phattalung', 'dest': 'Hat Yai Junction'}],
                            '2F': [{'origin': 'Bangkok', 'dest': 'Phetchaburi'},
                                   {'origin': 'Hua Hin', 'dest': 'Hat Yai Junction'}],
                            '2G': [],
                            '2H': []}

        self.train_seat_classes = [1, 2]

        read_reserved_tickets('south_reserved_tickets.txt', self.train_seats)

    def test_get_station_index(self):
        for i in range(TOTAL_NUM_STATIONS):
            station_name = list(self.station_indexes.keys())[i]
            output = get_station_index(self.station_indexes, station_name)
            self.assertEqual(i, output)

    def test_get_station_name(self):
        for i in range(TOTAL_NUM_STATIONS):
            station_name = list(self.station_indexes.keys())[i]
            output = get_station_name(self.station_indexes, i)
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

    # def get_ticket_price(self):
        # base case


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