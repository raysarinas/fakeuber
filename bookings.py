# 3 - BOOK MEMBERS OR CANCEL BOOKINGS

import re
from clear import clear
def getBookings(loginEmail, cursor, conn):
    print('Offer/Cancel a Booking')
    print('-----------------------------------------------------------')
    print('1 - Book a member')
    print('2 - Cancel a booking')
    print('3 - Go Back')
    while True:
        try:
            choice = int(input('Please enter 1, 2 or 3: '))
        except ValueError:
            print('Not a number. Do it again')
            continue
        # Member wants to book another member on a ride
        if choice == 1:
            bookBooking(loginEmail, cursor, conn)
            break
        # Member wants to cancel one of their bookings
        elif choice == 2:
            cancelBooking(loginEmail, cursor, conn)
            break
        # Member wants to go back to main selection screen
        elif choice == 3:
            break
        # Some other input was entered
        else:
            print('Invalid choice. Do it again')
            continue


def bookBooking(loginEmail, cursor, conn):
    print('Your Rides Offered:')
    counter = 0
    userOffers = None
    # Get number of rides the logged in user offers
    cursor.execute('''SELECT COUNT(*)
                             FROM rides r WHERE driver LIKE ?;''',(loginEmail,))
    totalRides = cursor.fetchone()
    totalRidesNum = totalRides[0]
    while True:
        # If we are not at past the length of our list
        if counter < totalRidesNum:
            # Select 5 rides offered and available seats per ride
            cursor.execute('''SELECT DISTINCT r.*, r.seats-IFNULL(SUM(b.seats),0) as available
                                                  FROM bookings b, rides r WHERE driver LIKE ?
                                                  AND r.rno = b.rno
                                                  GROUP BY r.rno
                                                  LIMIT ?,5;''', (loginEmail,counter))
            userOffers = cursor.fetchall()
            # In the situation where user has offered a ride but has no bookings do a special booking
            if not userOffers:
                print('You currently have no bookings. Let us make a new one')
                specialBooking(loginEmail, cursor, conn)
                break # return to main selection screen or logout


            # Print out the 5 or less matching rides offered
            print(" RNO | Price | Ride Date | Total Seats | Luggage description | Source | Destination | Driver | CarNum | Available Seats")
            for row in userOffers:
                print(str(row[0]) + " | " + str(row[1]) + " | " + str(row[2]) + " | " + str(row[3]) + " | ", end='')
                print(str(row[4]) + " | " + str(row[5]) + " | " + str(row[6]) + " | " + str(row[7]) + " | ", end='')
                print(str(row[8]) + " | " + str(row[9]))
        # End of list or no rides offered
        else:
            # No rides offered
            if userOffers is None:
                print('You are not currently offering any rides')
                break
            # End of the list
            else:
                print("End of List")
        selectMore = input('Enter "NEXT" to see more rides, "BOOK" to book a member on your ride, "EXIT" to exit this section: ').upper()
        # Member wants to see next 5 rides they offer
        if selectMore == "NEXT":
            counter += 5
            continue
        # Member wants to book a member on one of the current 5 or less ride shown
        elif selectMore == "BOOK":
            getBookingInfo(loginEmail, userOffers, cursor, conn)
            break
        # Member wants to exit
        elif selectMore == "EXIT":
            break
        else:
            print('Invalid command entered. Try again')

def specialBooking(loginEmail, cursor, conn):
    cursor.execute(''' SELECT rides.rno, rides.src, rides.dst, rides.seats FROM rides WHERE driver = ?''', (loginEmail,))
    fetched = cursor.fetchall()
    ride = fetched[0] # Get the first ride
    # Assign rno, pickup, dropoff, total seats and max bno for the first ride
    rno = ride[0]
    pickup = ride[1]
    dropoff = ride[2]
    seats = int(ride[3])
    cursor.execute('''SELECT MAX(bno)+1 as lastNum FROM bookings''')
    maxBno = cursor.fetchone()
    maxBno = maxBno[0]
    # Get number of seats they want booked
    checkValid = 0
    while True:
        try:
            numSeatsBook = int(input('Enter # of seats you want to book: '))
        except ValueError: # Value entered was not an integer
            print('Not a number. Do it again')
            continue
        if numSeatsBook <= 0: # Negative or 0 was entered, not allowed
            print('Invalid number of seats booked. Try again')
            continue
        # Check for warning of overbooked seats
        if numSeatsBook > seats:
            print("Warning! There are overbooked seats on this ride")
        break

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
    while True:
        try:
            costPerSeat = int(input('Enter the cost per seat (Must be an integer): '))
        except ValueError: # Value entered was not an integer
            print('Number entered is not an integer. Try Again.')
            continue
        if costPerSeat > 0: # Value entered is not 0 or negative, so good
            break
        else:
            print('Please enter a non-negative value greater than zero')
            continue
    # Add the booking
    cursor.execute(''' INSERT INTO bookings VALUES (?,?,?,?,?,?,?);''', (maxBno,emailMember,rno,costPerSeat,numSeatsBook,pickup,dropoff))
    conn.commit()
    print('Booking has been created')


def getBookingInfo(loginEmail, userOffers, cursor, conn):
    # Get pickup and dropoff location codes
    goodLCode = 0
    rno = None
    while True:
        pickUp = input('Enter the pickup location code: ').lower()
        dropOff = input('Enter the dropoff location code: ').lower()
        for x in userOffers:
            if x[5] == pickUp:
                goodLCode +=1
            if x[6] == dropOff:
                goodLCode +=1
            if goodLCode == 2: # If we have 2 then both lcodes match a specific ride
                # Get the rno of this selected lcodes
                rno = x[0]
                break
        if not rno: # If we were unable to get a rno, user must try again
            print('Invalid Location codes entered')
            goodLCode = 0
            continue
        else:
            break
    # Get number of seats they want booked
    checkValid = 0
    while True:
        try:
            numSeatsBook = int(input('Enter # of seats you want to book: '))
        except ValueError:
            print('Not a number. Do it again')
            continue
        if numSeatsBook <= 0:
            print('Invalid number of seats booked. Try again')
            continue
        # Find corresponding rno
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
            print('Error occured. Try again')
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
    while True:
        try:
            costPerSeat = int(input('Enter the cost per seat (Must be an integer): '))
        except ValueError:
            print('Number entered is not an integer. Try Again.')
            continue
        if costPerSeat > 0:
            break
        else:
            print('Please enter a non-negative value greater than zero')
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
    content = 'You have been booked on ride ' + str(rno) + ' by ' + loginEmail
    cursor.execute('''INSERT INTO inbox VALUES (?, datetime('now'), ?, ?, ?, 'n');''', (emailMember, loginEmail, content, rno))
    conn.commit()
    clear()
    print(emailMember, 'has been booked on ride #', rno)

def cancelBooking(loginEmail, cursor, conn):
    print('Your Current Bookings:')
    print('BNO | Member Email | RideNum | Cost Per Seat | Seats Booked | Pickup | Dropoff')
    cursor.execute('''SELECT DISTINCT b.* FROM bookings b, rides r WHERE driver LIKE ? AND b.rno=r.rno;''', (loginEmail,))
    userBookings = cursor.fetchall()
    # If they have any bookings
    if userBookings:
        # Print all of their bookings they have
        for row in userBookings:
            print(str(row[0]) + " | " + str(row[1]) + " | " + str(row[2]) + " | " + str(row[3]) + " | ", end='')
            print(str(row[4]) + " | " + str(row[5]) + " | " + str(row[6]))
        while True:
            try:
                cancelBno = int(input('Enter the bno of the booking you wish to cancel: '))
            except ValueError:
                print('Not a number. Do it again')
                continue
            # Find the bno that the member wants yo cancel
            cursor.execute('''SELECT * FROM bookings b, rides r where bno=? and b.rno=r.rno and driver LIKE ?;''', (cancelBno,loginEmail))
            cancelSelected = cursor.fetchone()
            # Check if selected bno exists, if not they have to try again
            if not cancelSelected:
                print('Booking selected does not exist')
                continue
            # Get content of message to send to other member
            content = input('Explain reason for cancelation: ')
            # Send message to member that their booking is cancelled
            cursor.execute('''INSERT INTO inbox VALUES (?,
                              datetime('now'), ?, ?, ?, 'n');''',(cancelSelected[1], loginEmail, content, cancelSelected[2]))
            conn.commit()
            # Delete selected booking
            cursor.execute('''DELETE FROM bookings WHERE bno=?;''', (cancelBno,))
            clear()
            print('Booking', cancelBno, 'has been cancelled.',cancelSelected[1], 'will be notified of the cancellation')
            conn.commit()
            break
    else:
        print('You have no bookings.')
