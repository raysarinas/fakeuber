# 3 - BOOK MEMBERS OR CANCEL BOOKINGS
def getBookings(loginEmail, cursor, conn):
    print('Offer/Cancel a Booking')
    print('-----------------------------------------------------------')
    print('1 - Book a member')
    print('2 - Cancel a booking')
    while True:
        choice = int(input('Please enter 1 or 2: '))
        if choice == 1:
            cancelBooking(loginEmail, cursor, conn)
            break
        else if choice == 2:
            bookBooking(loginEmail, cursor, conn)
            break
        else:
            print('Invalid choice dumbass do it again')
            continue

def bookBooking(loginEmail, cursor, conn):
    ajabdvkiasdvkjasdbvkjasbv

def cancelBooking(loginEmail, cursor, conn):
    siduvsdkjbviusdjnvsdiuv
