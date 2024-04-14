import hotel

with open('fund.txt', 'r', encoding='utf8') as fund:
    hotel_room = fund.readlines()
    # for room in hotel_room:


with open('booking.txt', 'r', encoding='utf8') as f_booknig:
    visiting = f_booknig.readlines()
    for visitors in visiting:
        visitors = visitors.strip().split(' ')
        name = visitors[1] + visitors[2] + visitors[3]
        booking = hotel.Hotel(visitors[0], name, visitors[4], visitors[5], visitors[6], visitors[7])
