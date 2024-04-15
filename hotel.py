import random


class Hotel:
    room_rate = {'одноместный': 2900, 'двухместный': 2300, 'полулюкс': 3200, 'люкс': 4100}
    coefficient_increase = {'стандарт': 1, 'стандарт_улучшенный': 1.2, 'апартамент': 1.5}
    type_nutrition = {'Без питания': 0, 'Завтрак': 2800, 'Полупансион': 1000}
    rooms_catalog = {}
    occupancy_rooms = {}
    current_date = ''
    lost_revenue = 0
    day_revenue = 0

    def __init__(self, current_date):
        Hotel.current_date = current_date

    @staticmethod
    def day_report():
        free_rooms = 0
        occupied_rooms = 0
        for key in Hotel.occupancy_rooms:
            if int(Hotel.current_date[:2]) not in Hotel.occupancy_rooms[key]:
                free_rooms += 1
            else:
                occupied_rooms += 1

        print(f'----- Отчет рабочего дня {Hotel.current_date} -----')
        print(f'Количество занятых номеров: {occupied_rooms}')
        print(f'Количество свободных номеров: {free_rooms}')
        print(f'Процент загруженности отдельных категорий номеров: ')
        print(f'Процент загруженности гостиницы в целом: {occupied_rooms / (free_rooms + occupied_rooms) * 100} %')
        print(f'Полученный доход за день: {Hotel.day_revenue}')
        print(f'Упущенный доход: {Hotel.lost_revenue}')
        print('\n')

    @staticmethod
    def add_rooms(number, kind, capacity, comfort):
        Hotel.rooms_catalog[number] = [kind, capacity, comfort]
        Hotel.occupancy_rooms[number] = []

    @staticmethod
    def date_shift(new_date):
        Hotel.current_date = new_date
        Hotel.day_revenue = 0
        Hotel.lost_revenue = 0


class PlacementOption:
    found_option = []

    def __init__(self, guest_quantity, stray_days, max_price):
        self.guest_quantity = guest_quantity
        self.stray_days = stray_days
        self.max_price = max_price

    def finding_option(self):
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
                                          Hotel.coefficient_increase[Hotel.rooms_catalog[key][2]]
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
    quantity = {'1': 'один', '2': 'два', '3': 'три', '4': 'четыре', '5': 'пять', '6': 'шесть', '7': 'семь'}
    probability_failure = [1, 0, 0, 0]

    def __init__(self, booking_date, name, quantity_people, check_in_date, quantity_days, acceptable_price):
        self.booking_date = booking_date
        self.name = name
        self.quantity_people = quantity_people
        self.check_in_date = check_in_date
        self.quantity_days = quantity_days
        self.acceptable_price = acceptable_price
        self.living_days = list(range(int(check_in_date[:2]), int(check_in_date[:2]) + int(quantity_days)))
        self.living_month = check_in_date[2:]
        self.living_dates = []
        for elem in self.living_days:       # ???7
            self.living_dates.append(str(elem) + self.living_month)

    def __str__(self):
        return f""" \n
        Заявка на бронь:
Имя: {self.name}
Дата бронирования - {self.booking_date}
Будет заселено человек: {BookingRequest.quantity[self.quantity_people]} 
на {BookingRequest.quantity[self.quantity_days]} дня: {self.living_dates}
Максимальный допустимый расход {self.acceptable_price} руб. на одного человека. \n"""

    def choosing_option(self):
        best_option = PlacementOption(self.quantity_people, self.living_days, self.acceptable_price)
        best_option.finding_option()
        if best_option.finding_option() is None:
            Hotel.lost_revenue += int(self.acceptable_price)
            return 'Нет подходящего номера'
        else:
            if random.choice(BookingRequest.probability_failure) == 0:
                Hotel.day_revenue += best_option.finding_option()[4]
                Hotel.occupancy_rooms[best_option.finding_option()[0]].append(self.living_days)
                return f'''Подобранный номер: {best_option.finding_option()[0]} 
Параметры: - {best_option.finding_option()[1]}
           - {best_option.finding_option()[2]}
           - {best_option.finding_option()[3]}
Стоимость: {best_option.finding_option()[4]} \n'''

            else:
                Hotel.lost_revenue += int(self.acceptable_price)
                return 'Гость сам отказался от своей брони'


