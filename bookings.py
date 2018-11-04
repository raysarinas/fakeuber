# 3 - BOOK MEMBERS OR CANCEL BOOKINGS
'''
https://stackoverflow.com/questions/26451888/sqlite-get-x-rows-then-next-x-rows
'''
import re
def getBookings(loginEmail, cursor, conn):
    print('Offer/Cancel a Booking')
    print('-----------------------------------------------------------')
    print('1 - Book a member')
    print('2 - Cancel a booking')
    while True:
        choice = int(input('Please enter 1 or 2: '))
        if choice == 1:
            bookBooking(loginEmail, cursor, conn)
            break
        elif choice == 2:
            cancelBooking(loginEmail, cursor, conn)
            break
        else:
            print('Invalid choice dumbass do it again')
            continue

def bookBooking(loginEmail, cursor, conn):
    print('Your Rides Offered:')
    counter = 0
    cursor.execute('''SELECT COUNT(*)
                             FROM bookings b, rides r WHERE driver LIKE ?
                             AND b.rno=r.rno;''',(loginEmail,))
    totalRides = cursor.fetchone()
    totalRidesNum = totalRides[0]
    while True:
        if counter < totalRidesNum:
            cursor.execute('''SELECT DISTINCT r.*, r.seats-IFNULL(SUM(b.seats),0) as available
                                                  FROM bookings b, rides r WHERE driver LIKE ?
                                                  AND b.rno=r.rno
                                                  GROUP BY r.rno
                                                  LIMIT ?,5;''', (loginEmail,counter))
            userOffers = cursor.fetchall()
            for x in userOffers:
                print(x, 'Available Seats: ', x[9])
                #print('''Price: ? Ride Date: ? Num of seats: ? Source: ? Dest: ? Seats available: ?
                        #''',(x['price'],x['rdate'],x['seats'],x['src'],x['dst'],x['available']))
        else:
            print("End of List")
        selectMore = input('Enter "NEXT" to see more rides, "BOOK" to book a member on your ride: ').upper()
        if selectMore == "NEXT":
            counter += 5
            continue
        elif selectMore == "BOOK":
            getBookingInfo(loginEmail, userOffers, cursor, conn)
        elif selectMore == "EXIT":
            break
        else:
            print('Invalid command entered. Try again')

def getBookingInfo(loginEmail, userOffers, cursor, conn):
    rno, numSeatsBook = 0
    emailMember, pickUp, dropOff = None
    # User enters ride # they want associated with new booking
    while True:
        rno = int(input('Enter Ride #: '))
        numSeatsBook = int(input('Enter # of seats you want to book: '))
        for x in userOffers:
            if rno == x["rno"]:
                if numSeatsBook > x["available"]:
                    print("Warning! There are overbooked seats on this ride")
                break
        continue

	# User enters member's email
    while True:
    	emailMember = input('Enter the email of the member you want to book: ')
    	emailCheck = re.match("^[_\d\w]+\\@[_\d\w]+\.[_\d\w]+$", email)
    	# Check valid email
    	if emailCheck is None:
    		print('Not an email. Try Again')
    		continue
    	cursor.execute('SELECT * FROM members WHERE email LIKE ?;', (emailMember,))
    	emails = cursor.fetchall()
    	if emails is None:
    		print('Member does not exist. Use a different email')
    		continue
    	else:
    		print('Valid email')
    		break
    # Get cost per seat
    costPerSeat = int(input('Enter the cost per seat: '))
    # Get pickup and dropoff location codes
    while True:
        pickUp = input('Enter the pickup location code: ')
        dropOff = input('Enter the dropoff location code: ')
        cursor.execute('''SELECT src, dst FROM rides WHERE rno=?''', (rno,))
        locationCodes = cursor.fetchone()
        if locationCodes[0] != pickUp:
            print('Invalid pickup code.')
            continue
        if locationCodes[1] != dropOff:
            print('Invalid dropoff code.')
            continue
        break

    cursor.execute('''SELECT MAX(bno)+1 as lastNum FROM bookings''')
    maxBno = cursor.fetchone()
    maxBno = maxBno[0]
    cursor.execute('''INSERT INTO bookings VALUES
                        (?, ?, ?, ?, ?, ?, ?)''',(maxBno, emailMember, rno, costPerSeat, numSeatsBook, pickUp, dropOff))
    cursor.execute('''INSERT INTO inbox VALUES (?, datetime('now'), 'You have been booked on the following ride'
                                        , 'n');''', (emailMember, loginEmail, rno))
    conn.commit()

def cancelBooking(loginEmail, cursor, conn):
    print('Your Current Bookings:')
    cursor.execute('''SELECT DISTINCT b.* FROM bookings b, rides r WHERE driver LIKE ? AND b.rno=r.rno;''', (loginEmail,))
    userBookings = cursor.fetchall()
    if userBookings:
        print(userBookings)
    else:
        print('You have no bookings.')
    while True:
        cancelBno = int(input('Enter the bno of the booking you wish to cancel: '))
        cursor.execute('''SELECT * FROM bookings where bno=? and driver LIKE ?;''', (cancelBno,loginEmail))
        cancelSelected = cursor.fetchone()
        if not cancelSelected:
            print('Booking selected does not exist')
            continue
        content = input('Explain reason for cancelation: ')
        cursor.execute('''INSERT INTO inbox VALUES (?,
                          datetime('now'), ?, ?, ?, 'n');''',(cancelSelected[1], loginEmail, content, cancelSelected[2]))
        cursor.execute('''DELETE FROM bookings WHERE bno=?;''', (cancelBno,))
        print('Booking ? has been cancelled. ? will be notified of the cancellation', (cancelBno, cancelSelected[1]))
        conn.commit()
