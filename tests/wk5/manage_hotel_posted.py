def read_file(filename):
    """ Read file with filename
        Read one line as one string and return nested list.
        Each line contains 5 values: floor number (int), room number (int),
        guest name (string), check-in date (int), and check-out date (int)

    :param filename: string
    :return: nested list of values from file
    """
    lines = open(filename).read().splitlines()
    booking_table = [x.split(",") for x in lines if x != ""]
    for row in booking_table:
        row[0] = int(row[0])
        row[1] = int(row[1])
        row[3] = int(row[3])
        row[4] = int(row[4])
    return booking_table


def initialize_str_nested_list(num_rows, num_cols):
    """ Construct a nested list with size = num_rows x num_cols
        Initialize all values inside this constructed nested list to be all
        empty strings

        :param num_rows: int
        :param num_cols: int
        :return: nested list of empty string with size num_rows x num_cols
        >>> initialize_str_nested_list(2,2)
        [['', ''], ['', '']]
        >>> initialize_str_nested_list(2,3)
        [['', '', ''], ['', '', '']]
        >>> initialize_str_nested_list(3,2)
        [['', ''], ['', ''], ['', '']]
    """
    init_list = []
    for row in range(num_rows):
        _list = []
        for col in range(num_cols):
            _list += [""]
        init_list += [_list]
    return init_list


def initialize_int_nested_list(num_rows, num_cols):
    """ Construct a nested list with size = num_rows x num_cols
        Initialize all values inside this constructed nested list to be all
        zeros

        :param num_rows: int
        :param num_cols: int
        :return: nested list of zeros with size = num_rows x num_cols
        >>> initialize_int_nested_list(2,2)
        [[0, 0], [0, 0]]
        >>> initialize_int_nested_list(2,3)
        [[0, 0, 0], [0, 0, 0]]
        >>> initialize_int_nested_list(3,2)
        [[0, 0], [0, 0], [0, 0]]
    """
    init_list = []
    for row in range(num_rows):
        _list = []
        for col in range(num_cols):
            _list += [0]
        init_list += [_list]
    return init_list


def get_booking_by_date(booking_table, num_floors, num_rooms, _date):
    """ From the given booking data from file, create 2 nested lists.  Each
        nested list has size = num_floors x num_rooms
    The first nested list shows which hotel room is booked on _date.
        Value = 1 if the room is booked. Otherwise, value = 0 for
        non-booked room.  For example, [[1, 0, 0], [0, 0, 1]] means that
        2 booked rooms are (floor 1, room 1) and (floor 2, room 3)
    The second nested list shows the guest names who books rooms on _date.
        For example [['Ann', '', ''], ['', '', 'Beth']] means that Ann books
        (floor 1, room 1) room, and Beth books (floor 2, room 3) room.

        :param booking_table: booking data from file
        :param num_floors: int
        :param num_rooms: int
        :param _date: int
        :return: two nested lists with size = num_rows x num_cols.
        The first nested list shows which hotel room is booked on _date
        The second nested list shows the guest names who books rooms on _date
        >>> get_booking_by_date([[1, 1, 'Ann', 21, 23], [2, 3, 'Beth', 22, 24]], 2, 3, 21)
        ([[1, 0, 0], [0, 0, 0]], [['Ann', '', ''], ['', '', '']])
        >>> get_booking_by_date([[1, 1, 'Ann', 21, 23], [2, 3, 'Beth', 22, 24]], 2, 3, 22)
        ([[1, 0, 0], [0, 0, 1]], [['Ann', '', ''], ['', '', 'Beth']])
        >>> get_booking_by_date([[1, 1, 'Ann', 21, 23], [2, 3, 'Beth', 22, 24]], 2, 3, 23)
        ([[0, 0, 0], [0, 0, 1]], [['', '', ''], ['', '', 'Beth']])
    """
    room_list = initialize_int_nested_list(num_floors, num_rooms)
    guest_list = initialize_str_nested_list(num_floors, num_rooms)
    for book_data in booking_table:
        if _date in range(book_data[3], book_data[4]):
            floor = book_data[0] - 1
            room = book_data[1] - 1
            room_list[floor][room] = 1
            guest_list[floor][room] = book_data[2]
    return room_list, guest_list


def draw_booking(curr_booking):
    """ Received the nested list shows which hotel room is booked on specific
    _date.
        Draw and show the booked hotel rooms according to choice 1.
        *** Partial code is given.  You also need to fill in some part on
        your own ***

        :param curr_booking: nested list shows which hotel room is booked on
                specific _date

    """
    cell_width = 3
    cell_height = 3
    print('|', end='')
    for j in range(len(curr_booking[0]) + 1):
        print('-' * cell_width + '|', end='')
    print()
    print('|   |', end='')
    for j in range(len(curr_booking[0])):
        print(f'{j + 1:^3}|', end='')
    print()
    print('|', end='')
    for j in range(len(curr_booking[0]) + 1):
        print('-' * cell_width + '|', end='')
    print()

    # HERE >>> Student fills more code below on your own
    for i in range(len(curr_booking)):
        print(f"|{i + 1:^3}|", end="")
        for k in range(len(curr_booking[i])):
            if curr_booking[i][k] == 1:
                print(" X |", end="")
            else:
                print("   |", end="")
        print()
        print("|", end="")
        for j in range(len(curr_booking[0]) + 1):
            print('-' * cell_width + '|', end='')
        print()


def get_booked_room_info_by_date(curr_booking, curr_guests):
    """ With two nested lists:
            The first nested list shows which hotel room is booked on
                specific _date,
            The second nested list shows the guest names who books rooms on
                specific _date
        Construct nested lists where each row contains 3 values: floor,
            room and guest name of the booked room.  See test outputs below.

        :param curr_booking: nested list of integers
        :param curr_guests: nested list of strings
        :return: nested lists where each row contains 3 values: floor, room and guest name of the booked room
        >>> get_booked_room_info_by_date([[1, 0, 0], [0, 0, 1]], [['Ann', '', ''], ['', '', 'Beth']])
        [[1, 1, 'Ann'], [2, 3, 'Beth']]
        >>> get_booked_room_info_by_date([[1, 0, 1], [0, 1, 0]], [['Ann', '', 'Beth'], ['', 'Cathy', '']])
        [[1, 1, 'Ann'], [1, 3, 'Beth'], [2, 2, 'Cathy']]
        >>> get_booked_room_info_by_date([[1, 1], [0, 1]], [['Charlie', 'David'], ['', 'Eric']])
        [[1, 1, 'Charlie'], [1, 2, 'David'], [2, 2, 'Eric']]
    """
    num_floors = len(curr_booking)
    num_rooms = len(curr_booking[0])
    booked_info = []
    for floor in range(num_floors):
        for room in range(num_rooms):
            if curr_booking[floor][room] == 1:
                guest_name = curr_guests[floor][room]
                booked_info += [[floor + 1, room + 1, guest_name]]
    return booked_info


def display_available_rooms(curr_booking):
    """Receive the nested list that shows which hotel room is booked on
      specfic date and display the available rooms in the format (floor,room)

    Expected output:
    >>> display_available_rooms([[1, 1, 0], [1, 0, 1]])
    Available rooms: (1,3), (2,2),
    >>> display_available_rooms([[0, 0, 1], [1, 1, 1]])
    Available rooms: (1,1), (1,2),
    >>> display_available_rooms([[1, 1, 1], [0, 0, 0]])
    Available rooms: (2,1), (2,2), (2,3),
    """
    num_floors = len(curr_booking)
    num_rooms = len(curr_booking[0])
    available = []
    for floor in range(num_floors):
        for room in range(num_rooms):
            if curr_booking[floor][room] == 0:
                available += [f"({floor + 1},{room + 1})"]

    print("Available rooms:", end="")
    for room in available:
        print(f" {room}", end=",")


def get_booked_room_info_by_floor(curr_booking, curr_guests, _floor):
    """ With two nested lists:
            The first nested list shows which hotel room is booked on
                specific _date,
            The second nested list shows the guest names who books rooms on
                specific _date
        and given _floor,
        Return nested list that contains information of floor, room and guest name
            of the booked room on such _floor

        :param curr_booking: nested list of integers
        :param curr_guests: nested list of strings
        :param _floor: int
        :return: nested lists where each row contains 3 values: floor, room and guest name of the booked room
        >>> get_booked_room_info_by_floor([[1, 0, 0], [0, 0, 1]], [['Ann', '', ''], ['', '', 'Beth']], 1)
        [[1, 1, 'Ann']]
        >>> get_booked_room_info_by_floor([[1, 0, 1], [0, 1, 0]], [['Ann','', 'Beth'], ['', 'Cathy', '']], 1)
        [[1, 1, 'Ann'], [1, 3, 'Beth']]
        >>> get_booked_room_info_by_floor([[1, 0, 1], [0, 1, 0]], [['Ann','', 'Beth'], ['', 'Cathy', '']], 2)
        [[2, 2, 'Cathy']]
    """
    num_rooms = len(curr_booking[0])
    booked_info = []
    for room in range(num_rooms):
        if curr_booking[_floor - 1][room] == 1:
            guest_name = curr_guests[_floor - 1][room]
            booked_info += [[_floor, room + 1, guest_name]]
    return booked_info


def get_booked_room_info_by_name(curr_booking, curr_guests, _name):
    """ With two nested lists:
            The first nested list shows which hotel room is booked on
                specific _date,
            The second nested list shows the guest names who books rooms on
                specific _date
        and a given _name,
        Return nested list that contains information of floor, room of the
            booked room and the guest name is _name

        :param curr_booking: nested list of integers
        :param curr_guests: nested list of strings
        :param _name: string
        :return: nested lists where each row contains 3 values: floor, room and guest name of the booked room
        >>> get_booked_room_info_by_name([[1, 0, 1], [0, 0, 1]], [['Ann', '', 'Beth'], ['', '', 'Ann']], 'Ann')
        [[1, 1, 'Ann'], [2, 3, 'Ann']]
        >>> get_booked_room_info_by_name([[1, 0, 1], [0, 0, 1]], [['Ann', '', 'Beth'], ['', '', 'Ann']], 'Beth')
        [[1, 3, 'Beth']]
        >>> get_booked_room_info_by_name([[1, 0, 1], [0, 0, 1]], [['Ann', '', 'Beth'], ['', '', 'Ann']], 'Charlie')
        []
    """
    num_floors = len(curr_booking)
    num_rooms = len(curr_booking[0])
    booked_info = []
    for floor in range(num_floors):
        for room in range(num_rooms):
            if curr_guests[floor][room] == _name:
                booked_info += [[floor + 1, room + 1, _name]]
    return booked_info


def count_booked_room_by_date(booking_table, _date):
    """ From the given booking data from file and specific _date,
        count and return number of booked room on the given _date

        :param booking_table: booking data from file
        :param _date: int
        :return: number of booked rooms on _date
        >>> count_booked_room_by_date([[1, 1, 'Ann', 21, 23], [2, 3, 'Beth', 22, 24]], 21)
        1
        >>> count_booked_room_by_date([[1, 1, 'Ann', 21, 23], [2, 3, 'Beth', 22, 24]], 22)
        2
        >>> count_booked_room_by_date([[1, 1, 'Ann', 21, 23], [2, 3, 'Beth', 22, 24]], 23)
        1
    """
    booked_num = 0
    for book_data in booking_table:
        if _date in range(book_data[3], book_data[4]):
            booked_num += 1
    return booked_num


def get_daily_revenue(booking_table, start_date, end_date):
    ''' From the given booking data from file and specific start_date and
    end_date,
        Return a list of daily revenue the hotel earns from the booked rooms.

        :param booking_table: booking data from file
        :param start_date: int
        :param end_date: int
        :return: a list of revenue from start_date to end_date (inclusive),
        where each room fee costs 2500 Baht per day.
        >>> get_daily_revenue([[1, 1, 'Ann', 21, 23], [2, 3, 'Beth', 22, 24]], 21, 22)
        [2500, 5000]
        >>> get_daily_revenue([[1, 1, 'Ann', 21, 23], [2, 3, 'Beth', 22, 24]], 21, 23)
        [2500, 5000, 2500]
        >>> get_daily_revenue([[1, 1, 'Ann', 21, 22], [2, 3, 'Beth', 23, 24]], 22, 23)
        [0, 2500]
    '''
    revenue = []
    for day in range(start_date, end_date + 1):
        booked_num = count_booked_room_by_date(booking_table, day)
        revenue += [booked_num * 2500]
    return revenue


def get_floor_revenue_by_date(booking_table, num_floors, current_date):
    ''' From the given booking data from file and specific current_date,
        Return a list of revenue separated by each floor.

        :param booking_table: booking data from file
        :param num_floors: int
        :param current_date: int
        :return: a list of revenue on a current_date but separated by each floor
        where each room fee costs 2500 Baht per day.
        >>> get_floor_revenue_by_date([[1, 1, 'Ann', 21, 23], [2, 3, 'Beth', 21, 24]], 2, 21)
        [2500, 2500]
        >>> get_floor_revenue_by_date([[1, 1, 'Ann', 21, 23], [1, 3, 'Beth', 22, 24]], 2, 22)
        [5000, 0]
        >>> get_floor_revenue_by_date([[1, 1, 'Ann', 21, 22], [2, 3, 'Beth', 23, 24]], 2, 23)
        [0, 2500]
    '''
    revenue = []
    for num_floor in range(1, num_floors + 1):
        book_floor_table = []
        for book_data in booking_table:
            if book_data[0] == num_floor:
                book_floor_table += [book_data]
        book_count = count_booked_room_by_date(book_floor_table, current_date)
        revenue += [book_count * 2500]
    return revenue


def get_room_revenue_by_date(booking_table, num_rooms, current_date):
    ''' From the given booking data from file and specific current_date,
        Return a list of revenue separated by each room section.

        :param booking_table: booking data from file
        :param num_rooms: int
        :param current_date: int
        :return: a list of revenue on a current_date but separated by each
        room section where each room fee costs 2500 Baht per day.
        >>> get_room_revenue_by_date([[1, 1, 'Ann', 21, 23], [2, 3, 'Beth', 21, 24]], 3, 21)
        [2500, 0, 2500]
        >>> get_room_revenue_by_date([[1, 1, 'Ann', 21, 23], [1, 3, 'Beth', 22, 24]], 3, 22)
        [2500, 0, 2500]
        >>> get_room_revenue_by_date([[1, 1, 'Ann', 21, 22], [2, 3, 'Beth', 23, 24]], 3, 23)
        [0, 0, 2500]
    '''
    if num_rooms == 3:
        num_floors = 2
    else:
        num_floors = 3
    curr_booking, curr_guest = get_booking_by_date(booking_table, num_floors,
                                                   num_rooms, current_date)
    revenue = []
    for num_room in range(num_rooms):
        room_count = 0
        for num_floor in range(num_floors):
            if curr_booking[num_floor][num_room] == 1:
                room_count += 1
        revenue += [room_count * 2500]
    return revenue


def operate(booking_table, num_floors, num_rooms, choice):
    if choice == 1:
        current_date = int(input('Enter date: '))
        curr_booking, curr_guests = get_booking_by_date(booking_table,
                                                        num_floors, num_rooms,
                                                        current_date)
        draw_booking(curr_booking)
    elif choice == 2:
        current_date = int(input('Enter date: '))
        curr_booking, curr_guests = get_booking_by_date(booking_table,
                                                        num_floors, num_rooms,
                                                        current_date)
        booked_info = get_booked_room_info_by_date(curr_booking, curr_guests)
        for info in booked_info:
            print(f"Room ({info[0]}, {info[1]}, {info[2]}),")
    elif choice == 3:
        current_date = int(input('Enter date: '))
        curr_booking, curr_guests = get_booking_by_date(booking_table,
                                                        num_floors, num_rooms,
                                                        current_date)
        display_available_rooms(curr_booking)
    elif choice == 4:
        current_date = int(input('Enter date: '))
        floor_num = int(input("Enter floor: "))
        curr_booking, curr_guests = get_booking_by_date(booking_table,
                                                        num_floors, num_rooms,
                                                        current_date)
        booked_info = get_booked_room_info_by_floor(curr_booking, curr_guests,
                                                    floor_num)
        for info in booked_info:
            print(f"Room ({info[0]}, {info[1]}, {info[2]}),")
    elif choice == 5:
        current_date = int(input('Enter date: '))
        guest_name = input("Enter guest name: ")
        curr_booking, curr_guests = get_booking_by_date(booking_table,
                                                        num_floors, num_rooms,
                                                        current_date)
        booked_info = get_booked_room_info_by_name(curr_booking, curr_guests,
                                                   guest_name)
        for info in booked_info:
            print(f"Room ({info[0]}, {info[1]}, {info[2]}),")
    elif choice == 6:
        start = int(input("Enter start date: "))
        end = int(input("Enter end date: "))
        revenue = get_daily_revenue(booking_table, start, end)
        for day in range(start, end + 1):
            print(f"{day}: {revenue[day - start]} Baht")
    elif choice == 7:
        current_date = int(input('Enter date: '))
        revenue = get_floor_revenue_by_date(booking_table, num_floors,
                                            current_date)
        print(f"Revenue for date {current_date}")
        for floor in range(num_floors):
            print(f"Floor {floor + 1}: {revenue[floor]} Baht")
    elif choice == 8:
        current_date = int(input('Enter date: '))
        revenue = get_room_revenue_by_date(booking_table, num_rooms,
                                           current_date)
        print(f"Revenue for date {current_date}")
        for section in range(num_rooms):
            print(f"Room-Section {section + 1}: {revenue[section]} Bath")

#
# num_floors = 2
# num_rooms = 3
# booking_table = read_file('hotel_small.txt')
# print(booking_table)

# Uncomment below if you want to test with hotel.txt
num_floors = 3
num_rooms = 5
booking_table = read_file('hotel.txt')

# print('1. Show booked rooms by date')
# print('2. Show guest names by date')
# print('3. Show available rooms by date')
# print('4. Show booked rooms by floor')
# print('5. Search booked room by name')
# print('6. Show daily revenue')
# print('7. Show floor revenue by date')
# print('8. Show room-section revenue by date')
# choice = int(input('Enter choice: '))
# operate(booking_table, num_floors, num_rooms, choice)

if __name__ == '__main__':
    import doctest

    doctest.testmod()
