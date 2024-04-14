import random


class Hotel:
    room_rate = {'одноместный': 2900, 'двухместный': 2300, 'полулюкс': 3200, 'люкс': 4100}
    coefficient_increase = {'стандарт': 1, 'стандарт_улучшенный': 1.2, 'апартамент': 1.5}
    type_nutrition = {'Без питания': 0, 'Завтрак': 2800, 'Полупансион': 1000}
    occupancy_rooms = {}
    for number_room in range(24):
        occupancy_rooms[str(number_room + 1)] = []
    quantity = {1: 'один', 2: 'два', 3: 'три', 4: 'четыре', 5: 'пять', 6: 'шесть'}

    def __init__(self, booking_date, name, quantity_people, check_in_date, quantity_days, acceptable_price):
        self.booking_date = booking_date
        self.name = name
        self.quantity_people = quantity_people
        self.check_in_date = check_in_date
        self.quantity_days = quantity_days
        self.acceptable_price = acceptable_price

    @classmethod
    def day_report(cls):
        print('-----Отчет рабочего дня-----')
        print('Количество занятых номеров: ')
        print('Количество свободных номеров: ')
        print('Процент загруженности отдельных категорий номеров: ')
        print('Процент загруженности гостиницы в целом: ')
        print('Полученный доход за день: ')
        print('Упущенный доход: ')

    def __str__(self):
        print(f'Дата бронирования - {self.booking_date}')
        if self.quantity_people == 1:
            print(f'Будет зачислен один человек на {Hotel.quantity[self.quantity_days]}')
        else:
            print(f'Будет заселено {Hotel.quantity[self.quantity_people]} человек на '
                  f'{Hotel.quantity[self.quantity_days]} дня: {[]}')
        print(f'Максимальный допустимый расход {self.acceptable_price} руб. на одного человека.')


class PlacementOption(Hotel):
    def __init__(self, room_number, room_type, maximum_room_capacity, degree_comfort, booking_date, name,
                 quantity_people, check_in_date, quantity_days, acceptable_price):
        super().__init__(booking_date, name, quantity_people, check_in_date, quantity_days, acceptable_price)
        self.room_number = room_number
        self.room_type = room_type
        self.maximum_room_capacity = maximum_room_capacity
        self.degree_comfort = degree_comfort


class BookingRequest:
    probability_failure = [1, 0, 0, 0]

    def __init__(self, booking_date, name, quantity_people, check_in_date, quantity_days, acceptable_price):
        self.booking_date = booking_date
        self.name = name
        self.quantity_people = quantity_people
        self.check_in_date = check_in_date
        self.quantity_days = quantity_days
        self.acceptable_price = acceptable_price
