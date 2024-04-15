import hotel

with open('fund.txt', 'r', encoding='utf8') as fund, open('booking.txt', 'r', encoding='utf8') as f_booking:
    visiting = f_booking.readlines()
    our_hotel = hotel.Hotel(visiting[0].split()[0])

    hotel_room = fund.readlines()
    for rooms in hotel_room:
        rooms = rooms.strip().split()
        hotel.Hotel.add_rooms(rooms[0], rooms[1], rooms[2], rooms[3])

    for visitors in visiting:
        visitors = visitors.strip().split(' ')
        if visitors[0] != our_hotel.current_date:
            our_hotel.day_report()
            our_hotel.date_shift(visitors[0])

        name = visitors[1] + ' ' + visitors[2] + ' ' + visitors[3]
        booking = hotel.BookingRequest(visitors[0], name, visitors[4], visitors[5], visitors[6], visitors[7])
        print(booking)
        print(booking.choosing_option())

    our_hotel.day_report()
