import random
import ru_local as ru


class Hotel:
    """
    A class that is modelling the day-to-day operation of the hotel.

    Attributes:
        room_rate : dict
            Types of hotel rooms by number of places and their prices.
        coefficient_increase : dict
            Types of hotel rooms according to the level of comfort and their coefficients that increase the base price.
        type_nutrition : dict
            Types of meals and their price.
        rooms_catalog :dict
            Catalogue containing all rooms by their serial number and information about their type.
        occupancy_rooms :dict
            Catalogue containing all rooms by their serial number and information about their occupancy on certain day.
        current_date : str
            The actual date of the hotel's day of operation.
        lost_revenue : int
            Revenue that was missed during the hotel's day of operation.
        day_revenue : int
            Revenue that was generated during the day of the hotel's operation.

    Methods:
        day_report():
            Creates and prints a report on the hotel's metrics and performance status for a single operating day.
        add_rooms():
            Adds a new room and its characteristics to the hotel room catalogue.
        date_shift():
            Changes the date when the hotel's operating day shifts.
    """

    room_rate = {ru.SINGLEROOM: 2900, ru.DOUBLEROOM: 2300, ru.JUNIOR_SUITE: 3200, ru.LUXURY: 4100}
    coefficient_increase = {ru.STANDART: 1, ru.STANDART_IMPROVED: 1.2, ru.APARTMENT: 1.5}
    type_nutrition = {ru.WITHOUT_POWER: 0, ru.BREAKFAST: 2800, ru.HALF_BOARD: 1000}
    rooms_catalog = {}
    occupancy_rooms = {}
    current_date = ''
    lost_revenue = 0
    day_revenue = 0

    def __init__(self, current_date):
        """
        Initializes a Hotel object.

        :param current_date: The actual date of the hotel's day of operation.
        :type current_date: str
        """

        Hotel.current_date = current_date

    @staticmethod
    def day_report():
        """
        Creates and prints a report on the hotel's metrics and performance status for a single operating day.

        :return: None
        """

        free_rooms = 0
        occupied_rooms = 0
        for key in Hotel.occupancy_rooms:
            if int(Hotel.current_date[:2]) not in Hotel.occupancy_rooms[key]:
                free_rooms += 1
            else:
                occupied_rooms += 1

        print(f'----- {ru.BUSINESS_DAY_REPORT} {Hotel.current_date} -----')
        print(f'{ru.NUMBER_OCCUPIED_ROOMS} {occupied_rooms}')
        print(f'{ru.NUMBER_AVAILBLE_ROOMS} {free_rooms}')
        print(f'{ru.PERCENTAGE_OCCUPANCY_TYPE_ROOMS} ')

        for key in Hotel.room_rate:
            total = 0
            occpd = 0
            for j in Hotel.rooms_catalog:
                if key in Hotel.rooms_catalog[j]:
                    if int(Hotel.current_date[:2]) in Hotel.occupancy_rooms[j]:
                        total += 1
                        occpd += 1
                    else:
                        total += 1
            print(f"{ru.OCCUPANCY_TYPE_ROOMS} '{key}' - {round(occpd/total * 100, 2)} %")

        for key in Hotel.coefficient_increase:
            total = 0
            occpd = 0
            for j in Hotel.rooms_catalog:
                if key in Hotel.rooms_catalog[j]:
                    if int(Hotel.current_date[:2]) in Hotel.occupancy_rooms[j]:
                        total += 1
                        occpd += 1
                    else:
                        total += 1
            print(f"{ru.OCCUPANCY_DEGREE_ROOMS} '{key}' - {round(occpd/total * 100, 2)} %")

        print(f'{ru.PERCENTAGE_OCCUPANCY_HOTEL} {round(occupied_rooms / (free_rooms + occupied_rooms) * 100, 2)} %')
        print(f'{ru.INCOME_DAY} {Hotel.day_revenue}')
        print(f'{ru.LOST_INCOME} {Hotel.lost_revenue}')
        print('\n')

    @staticmethod
    def add_rooms(number, kind, capacity, comfort):
        """
        Adds a new room and its characteristics to the hotel room catalogue.

        :param number: Hotel room serial number.
        :type number: str

        :param kind: The type of room regarding the number of places to be accommodated.
        :type kind: str

        :param capacity: Maximum number of guests for a one-time stay in a room.
        :type capacity: str

        :param comfort: Comfort level of the hotel room.
        :type comfort: str

        :return: None
        """

        Hotel.rooms_catalog[number] = [kind, capacity, comfort]
        Hotel.occupancy_rooms[number] = []

    @staticmethod
    def date_shift(new_date):
        """
        Changes the date when the hotel's operating day shifts.

        :param new_date: The new current date of the hotel's operating day.
        :type new_date: str

        :return: None
        """

        Hotel.current_date = new_date
        Hotel.day_revenue = 0
        Hotel.lost_revenue = 0


class PlacementOption:
    """
    A class that operates with all placement options and selects the optimal one regarding a given strategy.

    Attributes:
        found_option : list
            Optimal offer of a guest accommodation option, containing the characteristics of the selected room
            and the total cost.
        guest_quantity : str
            The number of guests from the booking request.
        stray_days : list
            The days of the month on which the guest will be staying in the hotel room.
        max_price : str
            The maximum sum of money the customer is willing to pay.

    Methods:
        finding_option():
            Finds the optimal room offer for the customer regarding the customer's requests and the hotel's
            current facilities.
    """

    found_option = []

    def __init__(self, guest_quantity, stray_days, max_price):
        """
        Initializes a PlacementOption object.

        :param guest_quantity: The number of guests from the booking request.
        :type guest_quantity: str

        :param stray_days: The days of the month on which the guest will be staying in the hotel room.
        :type stray_days: list

        :param max_price: The maximum sum of money the customer is willing to pay.
        :type max_price: str
        """

        self.guest_quantity = guest_quantity
        self.stray_days = stray_days
        self.max_price = max_price

    def finding_option(self):
        """
        Finds the optimal room offer for the customer regarding the customer's requests and the hotel's current
        facilities.

        :return: Optimal offer of a guest accommodation option, containing the characteristics of the selected room.
            and the total cost. Or None if there aren't any.
        :rtype: list
        """

        found_option = []

        for key, val in Hotel.occupancy_rooms.items():
            if not(any(elem in val for elem in self.stray_days)):
                if int(Hotel.rooms_catalog[key][1]) == int(self.guest_quantity):
                    required_amount = Hotel.room_rate[Hotel.rooms_catalog[key][0]] * \
                                      Hotel.coefficient_increase[Hotel.rooms_catalog[key][2]]
                    if required_amount <= int(self.max_price):
                        remain = int(self.max_price) - required_amount
                        nutrition = ''
                        price_scheduled_meals = 0
                        for food, price_food in Hotel.type_nutrition.items():
                            if price_food <= remain:
                                price_scheduled_meals = price_food
                                nutrition = food

                        found_option.append([key, Hotel.rooms_catalog[key][0], Hotel.rooms_catalog[key][2], nutrition,
                                             price_scheduled_meals + required_amount])

                elif not found_option:
                    if int(Hotel.rooms_catalog[key][1]) - int(self.guest_quantity) == 1:
                        required_amount = Hotel.room_rate[Hotel.rooms_catalog[key][0]] * \
                                          Hotel.coefficient_increase[Hotel.rooms_catalog[key][2]] * 0.7
                        if required_amount <= int(self.max_price):
                            remain = int(self.max_price) - required_amount
                            nutrition = ''
                            price_scheduled_meals = 0
                            for food, price_food in Hotel.type_nutrition.items():
                                if price_food <= remain:
                                    price_scheduled_meals = price_food
                                    nutrition = food

                            found_option.append(
                                [key, Hotel.rooms_catalog[key][0], Hotel.rooms_catalog[key][2], nutrition,
                                 price_scheduled_meals + required_amount])

        found_option = sorted(found_option, key=lambda x: x[4], reverse=True)

        if len(found_option) != 0:
            found_option = found_option[0]

        if len(found_option) == 0:
            return None
        else:
            return found_option


class BookingRequest:
    """
    A class that processes an incoming room reservation request.

    Attributes:
        quantity : dict
            Numbers in numeric format and their corresponding verbal spelling.
        probability_failure : list
            A list containing three 0's and a 1 to realise a 25% probability algorithm.
        booking_date : str
            The date on which the reservation request was created.
        name : str
            Customer's name.
        quantity_people : str
            The number of guests from the booking request.
        check_in_date : str
            The date of planned check-in to the hotel room.
        quantity_days : str
            Planned number of days of stay in the hotel room.
        acceptable_price : str
            The maximum sum of money the customer is willing to pay.

    Methods:
        choosing_option():
            Determines and prints the hotel offer in response to the customer's request and notices whether
            the booking has been confirmed or withdrawn.
    """

    quantity = {'1': ru.ONE, '2': ru.TWO, '3': ru.THREE, '4': ru.FOUR, '5': ru.FIVE, '6': ru.SIX, '7': ru.SEVEN}
    probability_failure = [1, 0, 0, 0]

    def __init__(self, booking_date, name, quantity_people, check_in_date, quantity_days, acceptable_price):
        """
        Initializes a BookingRequest object.

        :param booking_date: The date on which the reservation request was created.
        :type booking_date: str

        :param name: Customer's name.
        :type name: str

        :param quantity_people: The number of guests from the booking request.
        :type quantity_people: str

        :param check_in_date: The date of planned check-in to the hotel room.
        :type check_in_date: str

        :param quantity_days: Planned number of days of stay in the hotel room.
        :type quantity_days: str

        :param acceptable_price: The maximum sum of money the customer is willing to pay.
        :type acceptable_price: str
        """

        self.booking_date = booking_date
        self.name = name
        self.quantity_people = quantity_people
        self.check_in_date = check_in_date
        self.quantity_days = quantity_days
        self.acceptable_price = acceptable_price
        self.living_days = list(range(int(check_in_date[:2]), int(check_in_date[:2]) + int(quantity_days)))
        self.living_month = check_in_date[2:]
        self.living_dates = []
        for elem in self.living_days:
            self.living_dates.append(str(elem) + self.living_month)

    def __str__(self):
        return f""" \n
        {ru.BOOKING_REQUEST}
{ru.NAME} {self.name}
{ru.BOOKING_DATE} - {self.booking_date}
{ru.BOOKING_PEOPLE} {BookingRequest.quantity[self.quantity_people]}
{ru.DAY_BOOKED} {BookingRequest.quantity[self.quantity_days]}
{ru.ON} {ru.DATE} {self.living_dates}
{ru.MAX_CONSUMPTION} {self.acceptable_price} {ru.RUB} \n"""

    def choosing_option(self):
        """
        Determines and prints the hotel offer in response to the customer's request and notices whether
        the booking has been confirmed or withdrawn.

        :return: The hotel offer in response to the customer's request and a notice whether the booking has been
        confirmed or withdrawn.
        :rtype: str
        """

        best_option = PlacementOption(self.quantity_people, self.living_days, self.acceptable_price)
        result = best_option.finding_option()
        if result is None:
            Hotel.lost_revenue += int(self.acceptable_price)
            return f'{ru.NO_SUITEBLE_NUMBER} \n'
        else:
            if random.choice(BookingRequest.probability_failure) == 0:
                Hotel.day_revenue += result[4]
                Hotel.occupancy_rooms[result[0]].extend(self.living_days)
                return f'''{ru.SELECTED_NUMBER} {result[0]} 
{ru.PARAMETERS} - {result[1]}
           - {result[2]}
           - {result[3]}
{ru.COST} {result[4]} 

{ru.QUEST_CONFIRMED_RESERVATION} \n'''

            else:
                Hotel.lost_revenue += int(self.acceptable_price)
                return f'{ru.QUEST_REFUSED} \n'
