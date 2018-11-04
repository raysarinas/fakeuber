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
        try:
            choice = int(input('Please enter 1 or 2: '))
        except ValueError:
            print('Not a number. Do it again')
            continue
        if choice == 1:
            bookBooking(loginEmail, cursor, conn)
            break
        elif choice == 2:
            cancelBooking(loginEmail, cursor, conn)
            break
        else:
            print('Invalid choice. Do it again')
            continue


def bookBooking(loginEmail, cursor, conn):
    print('Your Rides Offered:')
    counter = 0
    # Get number of rides the logged in user offers
    cursor.execute('''SELECT COUNT(*)
                             FROM bookings b, rides r WHERE driver LIKE ?
                             AND b.rno=r.rno;''',(loginEmail,))
    totalRides = cursor.fetchone()
    totalRidesNum = totalRides[0]
    while True:
        # If we are not at past the length of our list
        if counter < totalRidesNum:
            # Select 5 rides offered and available seats per ride
            cursor.execute('''SELECT DISTINCT r.*, r.seats-IFNULL(SUM(b.seats),0) as available
                                                  FROM bookings b, rides r WHERE driver LIKE ?
                                                  AND b.rno=r.rno
                                                  GROUP BY r.rno
                                                  LIMIT ?,5;''', (loginEmail,counter))
            userOffers = cursor.fetchall()
            print(" RNO | Price | Ride Date | Total Seats | Luggage description | Source | Destination | Driver | CarNum | Available Seats")
            for x in userOffers:
                print(x)
        # End of list or no rides offered
        else:
            print("End of List")
        selectMore = input('Enter "NEXT" to see more rides, "BOOK" to book a member on your ride, "EXIT" to exit this section: ').upper()
        if selectMore == "NEXT":
            counter += 5
            continue
        elif selectMore == "BOOK":
            getBookingInfo(loginEmail, userOffers, cursor, conn)
            break
        elif selectMore == "EXIT":
            break
        else:
            print('Invalid command entered. Try again')


def getBookingInfo(loginEmail, userOffers, cursor, conn):
    # User enters ride # they want associated with new booking
    checkValid = 0
    while True:
        try:
            rno = int(input('Enter Ride #: '))
            numSeatsBook = int(input('Enter # of seats you want to book: '))
        except ValueError:
            print('Not a number. Do it again')
            continue
        # Check that rno exists
        for x in userOffers:
            if rno == x[0]:
                # Check for warning of overbooked seats
                if numSeatsBook > x[9]:
                    print("Warning! There are overbooked seats on this ride")
                checkValid += 1
                break
        if checkValid > 0:
            break
        # Ride did not exist
        else:
            print('Ride is not in current list')
            continue

	# User enters member's email
    while True:
    	emailMember = input('Enter the email of the member you want to book: ').lower()
    	emailCheck = re.match("^[_\d\w]+\\@[_\d\w]+\.[_\d\w]+$", emailMember)
    	# Check valid email
    	if emailCheck is None:
    		print('Not an email. Try Again')
    		continue
        # Check is member exists
    	cursor.execute('SELECT * FROM members WHERE email LIKE ?;', (emailMember,))
    	emails = cursor.fetchall()
    	if not emails:
    		print('Member does not exist. Use a different email')
    		continue
    	else:
    		break
    # Get cost per seat
    costPerSeat = int(input('Enter the cost per seat: '))
    # Get pickup and dropoff location codes
    goodLCode = 0
    while True:
        pickUp = input('Enter the pickup location code: ').lower()
        dropOff = input('Enter the dropoff location code: ').lower()
        cursor.execute('''SELECT lcode FROM locations''')
        locationCodes = cursor.fetchall()
        for x in locationCodes:
            if x[0] == pickUp:
                goodLCode +=1
            if x[0] == dropOff:
                goodLCode +=1
        if goodLCode == 2:
            break
        else:
            print('Invalid Location codes entered')
            continue
    # Get highest bno in bookings. Plus 1 would represent a unique bno
    cursor.execute('''SELECT MAX(bno)+1 as lastNum FROM bookings''')
    maxBno = cursor.fetchone()
    maxBno = maxBno[0]
    # Insert new booking into table
    cursor.execute('''INSERT INTO bookings VALUES
                        (?, ?, ?, ?, ?, ?, ?)''',(maxBno, emailMember, rno, costPerSeat, numSeatsBook, pickUp, dropOff))
    conn.commit()
    # Send message to member that they have been booked on this ride
    content = 'You have been booked on ride' + str(rno) + 'by' + loginEmail
    cursor.execute('''INSERT INTO inbox VALUES (?, datetime('now'), ?, ?, ?, 'n');''', (emailMember, loginEmail, content, rno))
    conn.commit()
    print(emailMember, 'has been booked on ride #', rno)

def cancelBooking(loginEmail, cursor, conn):
    print('Your Current Bookings:')
    print('BNO | Member Email | RideNum | Cost Per Seat | Seats Booked | Pickup | Dropoff')
    cursor.execute('''SELECT DISTINCT b.* FROM bookings b, rides r WHERE driver LIKE ? AND b.rno=r.rno;''', (loginEmail,))
    userBookings = cursor.fetchall()
    # If they have any bookings
    if userBookings:
        for x in userBookings:
            print(x)
        while True:
            try:
                cancelBno = int(input('Enter the bno of the booking you wish to cancel: '))
            except ValueError:
                print('Not a number. Do it again')
                continue

            cursor.execute('''SELECT * FROM bookings b, rides r where bno=? and b.rno=r.rno and driver LIKE ?;''', (cancelBno,loginEmail))
            cancelSelected = cursor.fetchone()
            if not cancelSelected:
                print('Booking selected does not exist')
                continue
            content = input('Explain reason for cancelation: ')
            # Send message to member that their booking is cancelled
            cursor.execute('''INSERT INTO inbox VALUES (?,
                              datetime('now'), ?, ?, ?, 'n');''',(cancelSelected[1], loginEmail, content, cancelSelected[2]))
            conn.commit()
            # Delete selected booking
            cursor.execute('''DELETE FROM bookings WHERE bno=?;''', (cancelBno,))
            print('Booking', cancelBno, 'has been cancelled.',cancelSelected[1], 'will be notified of the cancellation')
            conn.commit()
            break
    else:
        print('You have no bookings.')
