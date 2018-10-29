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
    pass #ajabdvkiasdvkjasdbvkjasbv

def cancelBooking(loginEmail, cursor, conn):
    print('Your Current Bookings:')
    cursor.execute('''SELECT DISTINCT * FROM bookings b, rides r WHERE driver=? AND b.rno=r.rno;''', (loginEmail,))
    userBookings = cursor.fetchall()
    print(userBookings)
    while True:
        cancelBno = int(input('Enter the bno of the booking you wish to cancel: '))
        cursor.execute('''SELECT * FROM bookings where bno=?;''', (cancelBno,))
        cancelSelected = cursor.fetchone()
        if not cancelSelected:
            print('Booking selected does not exist')
            continue
        content = input('Explain reason for cancelation: ')
        cursor.execute('''INSERT INTO inbox VALUES (?,
                          datetime('now'), ?, ?, ?, n);''',(cancelSelected["email"], loginEmail, content, cancelSelected["rno"]))
        cursor.execute('''DELETE FROM bookings WHERE bno=?;''', (cancelBno,))
        print('Booking ? has been cancelled. ? will be notified of the cancellation', ())
        conn.commit()
