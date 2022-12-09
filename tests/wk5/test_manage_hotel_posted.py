import unittest
import io
from unittest.mock import patch
from manage_hotel_posted import *
from difflib import SequenceMatcher


class TestManageHotel(unittest.TestCase):
    def setUp(self) -> None:
        self.booking_table = [[1, 1, "Jeff", 18, 20], [1, 2, "John", 13, 15],
                              [2, 2, "James", 19, 21], [2, 3, "Jack", 14, 19]]

        self.booking_table2 = [[1, 1, "Jeff", 18, 20], [1, 2, "John", 13, 15],
                               [1, 4, "Jump", 9, 12],
                               [2, 2, "James", 19, 21], [2, 3, "Jack", 14, 19],
                               [2, 5, "Jub", 22, 23],
                               [3, 1, "Kate", 25, 28], [3, 4, "Korn", 1, 5],
                               [3, 5, "Korn", 1, 5]]

    def test_init_str(self):
        str_1 = initialize_str_nested_list(2, 3)
        self.assertEqual(str_1, [['', '', ''], ['', '', '']],
                         "Initial string [1] is not correct")
        str_2 = initialize_str_nested_list(0, 0)
        self.assertEqual(str_2, [], "Initial string [2] is not correct")
        str_3 = initialize_str_nested_list(3, 4)
        self.assertEqual(str_3, [['', '', '', ''], ['', '', '', ''],
                                 ['', '', '', '']],
                         "Initial string [3] is not correct")

    def test_init_int(self):
        int_1 = initialize_int_nested_list(2, 3)
        self.assertEqual(int_1, [[0, 0, 0], [0, 0, 0]],
                         "Initial int [1] is not correct")
        int_2 = initialize_int_nested_list(0, 0)
        self.assertEqual(int_2, [], "Initial int [2] is not correct")
        int_3 = initialize_int_nested_list(3, 4)
        self.assertEqual(int_3, [[0, 0, 0, 0], [0, 0, 0, 0],
                                 [0, 0, 0, 0]],
                         "Initial int [3] is not correct")

    def test_get_book_by_date(self):
        room_l1, guest_l1 = get_booking_by_date(self.booking_table, 2, 3, 19)
        self.assertEqual(room_l1, [[1, 0, 0], [0, 1, 0]],
                         "Room list is not valid [1]")
        self.assertEqual(guest_l1, [['Jeff', '', ''], ['', 'James', '']],
                         "Guest list is not valid [1]")
        room_l2, guest_l2 = get_booking_by_date(self.booking_table, 2, 3, 14)
        self.assertEqual(room_l2, [[0, 1, 0], [0, 0, 1]],
                         "Room list is not valid [2]")
        self.assertEqual(guest_l2, [['', 'John', ''], ['', '', 'Jack']],
                         "Guest list is not valid [2]")
        room_l3, guest_l3 = get_booking_by_date(self.booking_table, 2, 3, 12)
        self.assertEqual(room_l3, [[0, 0, 0], [0, 0, 0]],
                         "Room list is not valid [3]")
        self.assertEqual(guest_l3, [['', '', ''], ['', '', '']],
                         "Guest list is not valid [3]")

        room, guest = get_booking_by_date(self.booking_table2, 3, 5, 4)
        self.assertEqual(room,
                         [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 1, 1]],
                         "Room list is not valid [4]")
        self.assertEqual(guest, [['', '', '', '', ''], ['', '', '', '', ''],
                                 ['', '', '', "Korn", "Korn"]],
                         "Guest list is not valid [4]")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_draw_booking_1(self, output):
        current_book, _ = get_booking_by_date(self.booking_table, 2, 3, 19)
        draw_booking(current_book)
        cor_output1 = "|---|---|---|---|\n" \
                      "|   | 1 | 2 | 3 |\n" \
                      "|---|---|---|---|\n" \
                      "| 1 | X |   |   |\n" \
                      "|---|---|---|---|\n" \
                      "| 2 |   | X |   |\n" \
                      "|---|---|---|---|\n"
        likeness = SequenceMatcher(None, output.getvalue(),
                                   cor_output1).ratio()
        self.assertGreaterEqual(likeness, 0.85, "Output is not correct")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_draw_booking_2(self, output):
        current_book, _ = get_booking_by_date(self.booking_table, 2, 3, 12)
        draw_booking(current_book)
        cor_output1 = "|---|---|---|---|\n" \
                      "|   | 1 | 2 | 3 |\n" \
                      "|---|---|---|---|\n" \
                      "| 1 |   |   |   |\n" \
                      "|---|---|---|---|\n" \
                      "| 2 |   |   |   |\n" \
                      "|---|---|---|---|\n"
        likeness = SequenceMatcher(None, output.getvalue(),
                                   cor_output1).ratio()
        self.assertGreaterEqual(likeness, 0.85, "Output is not correct")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_draw_booking_3(self, output):
        current_book, _ = get_booking_by_date(self.booking_table2, 3, 5, 3)
        draw_booking(current_book)
        cor_output1 = "|---|---|---|---|---|---|\n" \
                      "|   | 1 | 2 | 3 | 4 | 5 |\n" \
                      "|---|---|---|---|---|---|\n" \
                      "| 1 |   |   |   |   |   |\n" \
                      "|---|---|---|---|---|---|\n" \
                      "| 2 |   |   |   |   |   |\n" \
                      "|---|---|---|---|---|---|\n" \
                      "| 3 |   |   |   | X | X |\n" \
                      "|---|---|---|---|---|---|\n"
        likeness = SequenceMatcher(None, output.getvalue(),
                                   cor_output1).ratio()
        self.assertGreaterEqual(likeness, 0.80, "Output is not correct")

    def test_get_booked_room_info_by_date(self):
        room_l1, guest_l1 = get_booking_by_date(self.booking_table, 2, 3, 18)
        book_info = get_booked_room_info_by_date(room_l1, guest_l1)
        self.assertEqual(book_info, [[1, 1, "Jeff"], [2, 3, "Jack"]],
                         "Room info is not correct.")
        room_l2, guest_l2 = get_booking_by_date(self.booking_table, 2, 3, 14)
        book_info2 = get_booked_room_info_by_date(room_l2, guest_l2)
        self.assertEqual(book_info2, [[1, 2, "John"], [2, 3, "Jack"]],
                         "Room info is not correct.")
        room_l3, guest_l3 = get_booking_by_date(self.booking_table, 2, 3, 12)
        book_info3 = get_booked_room_info_by_date(room_l3, guest_l3)
        self.assertEqual(book_info3, [], "Room info is not correct.")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_display_available_rooms_1(self, output):
        curr_book, _ = get_booking_by_date(self.booking_table, 2, 3, 18)
        display_available_rooms(curr_book)
        cor_output = "Available rooms: (1,2), (1,3), (2,1), (2,2),"
        likeness = SequenceMatcher(None, output.getvalue(), cor_output).ratio()
        self.assertGreaterEqual(likeness, 0.85, "Output is not correct")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_display_available_rooms_2(self, output):
        curr_book, _ = get_booking_by_date(self.booking_table, 2, 3, 12)
        display_available_rooms(curr_book)
        cor_output = "Available rooms: (1,1), (1,2), (1,3), (2,1), (2,2), (2,3),"
        likeness = SequenceMatcher(None, output.getvalue(), cor_output).ratio()
        self.assertGreaterEqual(likeness, 0.85, "Output is not correct")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_display_available_rooms_3(self, output):
        curr_book, _ = get_booking_by_date(self.booking_table2, 3, 5, 11)
        display_available_rooms(curr_book)
        cor_output = "Available rooms: (1,1), (1,2), (1,3), (1,5), " \
                     "(2,1), (2,2), (2,3), (2,4), (2,5), " \
                     "(3,1), (3,2), (3,3), (3,4), (3,5)"
        likeness = SequenceMatcher(None, output.getvalue(), cor_output).ratio()
        self.assertGreaterEqual(likeness, 0.85, "Output is not correct")

    def test_get_booked_room_info_by_floor(self):
        room_l1, guest_l1 = get_booking_by_date(self.booking_table, 2, 3, 19)
        book_info = get_booked_room_info_by_floor(room_l1, guest_l1, 1)
        self.assertEqual(book_info, [[1, 1, "Jeff"]],
                         "Booked info is not correct.")
        book_info = get_booked_room_info_by_floor(room_l1, guest_l1, 2)
        self.assertEqual(book_info, [[2, 2, "James"]],
                         "Booked info is not correct.")

        room_l1, guest_l1 = get_booking_by_date(self.booking_table, 2, 3, 12)
        book_info = get_booked_room_info_by_floor(room_l1, guest_l1, 1)
        self.assertEqual(book_info, [], "Booked info is not correct.")
        book_info = get_booked_room_info_by_floor(room_l1, guest_l1, 2)
        self.assertEqual(book_info, [], "Booked info is not correct.")

        room, guest = get_booking_by_date(self.booking_table2, 3, 5, 3)
        book_info = get_booked_room_info_by_floor(room, guest, 3)
        self.assertEqual(book_info, [[3, 4, "Korn"], [3, 5, "Korn"]],
                         "Booked info is not correct. [5]")

    def test_get_booked_room_info_by_name(self):
        room_l1, guest_l1 = get_booking_by_date(self.booking_table, 2, 3, 19)
        book_info = get_booked_room_info_by_name(room_l1, guest_l1, "Jeff")
        self.assertEqual(book_info, [[1, 1, "Jeff"]],
                         "Book info is not correct")
        book_info = get_booked_room_info_by_name(room_l1, guest_l1, "Jummeng")
        self.assertEqual(book_info, [], "Book info is not correct [2]")

        room, guest = get_booking_by_date(self.booking_table2, 3, 5, 22)
        book_info = get_booked_room_info_by_name(room, guest, "Jub")
        self.assertEqual(book_info, [[2, 5, "Jub"]],
                         "Book info is not correct [3]")

    def test_count_booked_room_by_date(self):
        counted = count_booked_room_by_date(self.booking_table, 19)
        self.assertEqual(counted, 2, "Incorrect room counted [1]")

        counted = count_booked_room_by_date(self.booking_table, 13)
        self.assertEqual(counted, 1, "Incorrect room counted [2]")

        counted = count_booked_room_by_date(self.booking_table, 12)
        self.assertEqual(counted, 0, "Incorrect room counted [3]")

        counted = count_booked_room_by_date(self.booking_table2, 3)
        self.assertEqual(counted, 2, "Incorrect room counted [4]")

    def test_get_daily_revenue(self):
        rev = get_daily_revenue(self.booking_table, 13, 15)
        self.assertEqual(rev, [2500, 5000, 2500])

        rev = get_daily_revenue(self.booking_table, 19, 19)
        self.assertEqual(rev, [5000])

        rev = get_daily_revenue(self.booking_table, 10, 12)
        self.assertEqual(rev, [0, 0, 0])

        rev = get_daily_revenue(self.booking_table2, 20, 22)
        self.assertEqual(rev, [2500, 0, 2500])

    def test_get_floor_revenue_by_date(self):
        pass

    def test_get_room_revenue_by_date(self):
        pass

    def test_operate(self):
        pass


if __name__ == '__main__':
    unittest.main()
