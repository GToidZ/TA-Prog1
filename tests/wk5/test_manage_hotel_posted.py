import unittest
import io
from unittest.mock import patch
from manage_hotel_posted import *
from difflib import SequenceMatcher


class TestManageHotel(unittest.TestCase):
    def setUp(self) -> None:
        self.booking_table = [[1, 1, "Jeff", 18, 20], [1, 2, "John", 13, 15],
                              [2, 2, "James", 19, 21], [2, 3, "Jack", 14, 19]]

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
        likeness = SequenceMatcher(None, output.getvalue(), cor_output1).ratio()
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
        likeness = SequenceMatcher(None, output.getvalue(), cor_output1).ratio()
        self.assertGreaterEqual(likeness, 0.85, "Output is not correct")

    def test_get_booked_room_info_by_date(self):
        room_l1, guest_l1 = get_booking_by_date(self.booking_table, 2, 3, 18)
        book_info = get_booked_room_info_by_date(room_l1, guest_l1)
        self.assertEqual(book_info, [[1, 1, "Jeff"], [2, 3, "Jack"]])
        room_l2, guest_l2 = get_booking_by_date(self.booking_table, 2, 3, 14)
        book_info2 = get_booked_room_info_by_date(room_l2, guest_l2)
        self.assertEqual(book_info2, [[1, 2, "John"], [2, 3, "Jack"]])
        room_l3, guest_l3 = get_booking_by_date(self.booking_table, 2, 3, 12)
        book_info3 = get_booked_room_info_by_date(room_l3, guest_l3)
        self.assertEqual(book_info3, [])

    def test_display_available_rooms(self):
        pass

    def test_get_booked_room_info_by_floor(self):
        pass

    def test_get_booked_room_info_by_name(self):
        pass

    def test_count_booked_room_by_date(self):
        pass

    def test_get_daily_revenue(self):
        pass

    def test_get_floor_revenue_by_date(self):
        pass

    def test_get_room_revenue_by_date(self):
        pass

    def test_operate(self):
        pass


if __name__ == '__main__':
    unittest.main()
