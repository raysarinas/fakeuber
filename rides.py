# 1 - OFFER A RIDE
# 2 - SEARCH FOR RIDES
import sqlite3
import main, login, re
import time, datetime

def offerRide(cursor, conn, email):
    '''
    The member should be able to offer rides by providing a date, the number
    of seats offered, the price per seat, a luggage description,
    a source location, and a destination location. The member should have the
    option of adding a car number and any set of enroute locations. For
    locations (including source, destination and enroute), the member
    should be able to provide a keyword, which can be a location code. If the
    keyword is not a location code, your system should return all locations
    that have the keyword as a substring in city, province or address fields.
    If there are more than 5 matching locations, at most 5 matches will be
    shown at a time, letting the member select a location or see more matches.
    If a car number is entered, your system must ensure that the car belongs
    to the member. Your system should automatically assign a unique ride
    number (rno) to the ride and set the member as the driver of the ride.
    '''
    #clear()
    print('Offer a ride by entering the following information: ')

    while True:
        date = input('Ride Date (YYYY-MM-DD)?')
        dateCheck = re.match("^[\d]{4}\\-[\d]{2}\\-[\d]{2}$", date)
        if dateCheck is None:
            print('Invalid Date. Try Again')
            continue
        else: # CONVERT TO DATE TYPE
            year, month, day = map(int, date.split('-'))
            date = datetime.date(year, month, day)

        # CHECK THE NUMSEATS AND SEATPRICE INPUT HERE IF VALID DIGIT
        # @ JUJU : MOHAMMAD'S PARTNER DID THIS CHECK REAL SMART SO
        # I DID THE SAME BUT LIKE IF YOU CHANGE IT TO seats.isdigit != True
        # IT DOESNT WORK IDK WHY?????? PLS MSG ABOUT THIS WHEN U SEE IT
        seats = input("How many seats are you offering? ")
        while seats.isdigit == False:
            seats = input("Invalid input. Enter a numerical amount: ")
        seats = int(seats)

        price = input("What is the price per seat? ")
        while price.isdigit == False:
            price = input("Invalid input. Enter a numerical amount: ")
        price = int(price)

        luggage = input("Enter luggage description: ")
        while len(luggage) > 10:
            luggage = input("Desciption too long. Enter a shorter description: ")

        # CHECK LOCATION STUFFFFFFF
        source = getLocation(cursor, conn, email) #getLoc(cursor, conn, email).replace("%", "")
        dest = getLocation(cursor, conn, email) #getLoc(cursor, conn, email).replace("%", "")

        print("Would you like to add a car number? Enter 'Y' if yes. Otherwise, enter anything else. ")
        while True:
            cno = None # OR SHOULD THIS BE NULL????? # if did not want to enter a car num
            askCarNum = input()
            if askCarNum.lower() == 'y':
                cno = getCarNum(cursor, conn, email)
            else:
                break

        # while True:
        #     enroutes = []
        #     askEnroutes = input("Would you like to add any enroute locations? Enter 'Y' if yes. Otherwise, enter anything else.")
        #
        #     while askEnroutes.lower() == 'y':

        rno = getRNO(cursor, conn, email)

        cursor.execute('''INSERT INTO rides
                VALUES (?,?,?,?,?,?,?,?,?);''', (rno, price, date, seats, luggage, source, dest, email, cno))
        conn.commit()

        print('Ride Offering Posted!')

        break

def getCarNum(cursor, conn, email):
    carNum = input("Enter car number: ")
    while carNum.isdigit() == False:
        carNum = input("Incorrect input, please enter a number: ")
    carNum = int(carNum)
    cursor.execute("SELECT cno from cars where owner = ? and cno = ?", (email, carNum))
    if cursor.fetchone() == None or cursor.fetchone()[0] != carNum:
        print("Car is not registered with you, please try again by entering 'Y'. Otherwise, no.")
        carNum = None

        # GET STUCK IN LOOP IF DONT HAVE CAR NUMBER NEED WAY TO BREAK OUT OF IT???

def getRNO(cursor, conn, email):
    cursor.execute(''' SELECT MAX(rides.rno) FROM rides;''')
    last = cursor.fetchall()
    if last == None:
        return 1
    rno = int(last[0][0])+ 1
    return rno

# def getRideNum(cursor, conn, email):
#     cursor.execute("SELECT max(rno) from rides")
#     last = cursor.fetchone()
#     if last == None:
#         return 1
#     rno = last[0] + 1
#     return rno

# def offerRideOLD(cursor, conn, email):
#     date = input("Date of the ride: (YYYY-MM-DD): ")
#     if not checkValidDate(date):
#         print("Invalid format: PLease try again (YYYY-MM-DD)")
#         offerRide(cursor, conn, email)
#
#     numSeats = input("Enter number of seats: ")
#     validNumSeats(numSeats)
#
#     seatPrice = input("Enter price per seat: ")
#     validSeatPrice(seatPrice)
#
#     luggage = input("Enter luggage description: ") #fix luggage desc?????
#     print("Source Location")
#     sourceLoc = getLoc(cursor, conn, email).replace("%", "")
#     print("Destination Location")
#     destLoc = getLoc(cursor, conn, email).replace("%", "")
#     carNum = 'NULL' #if did not want to enter a car num
#     askCarNum = input("Would you like to add a car number? [Y/N]")
#     if askCarNum.upper() == 'Y':
#         carNum = getCarNum(cursor, conn, email)
#
#     # elif askCarNum.upper() == 'N':
#     #     enrouteSet = []
#     #     askEnroute = input("Would you like to add an enroute location? [Y/N]")
#     #     if askEnroute.upper() == 'Y':
#     #         addEnroute = getLoc(cursor, conn)
#     #         enrouteSet.append(addEnroute)
#     #         askEnrouteAgain = input ("Would you like to add another enroute location? [Y/N] ")
#
#     #rideNum = getRideNum(cursor, conn)
#
#     enrouteSet = []
#     askEnroute = input("Would you like to add an enroute location? [Y/N]")
#     if askEnroute.upper() == 'Y':
#         addEnroute = getLoc(cursor, conn, email)
#         enrouteSet.append(addEnroute)
#         askEnrouteAgain = input ("Would you like to add another enroute location? [Y/N] ")
#         #if askEnrouteAgain.upper() == 'Y':
#             #######fix this move this somewhere???
#     # elif askEnroute.upper() == 'N':
#     #     return
#     assignRideNum = getRideNum(cursor, conn, email)
#     if len(enrouteSet) != 0:
#         for loc in enrouteSet:
#             cursor.execute("INSERT INTO enroute values (?, ?)", (assignRideNum, loc))
#             connection.commit()
#     cursor.execute("INSERT INTO rides values (?, ?, ?, ?, ?, ?, ?, ?, ?)", (assignRideNum, seatPrice, date, numSeats, luggage, sourceLoc, destLoc, email, carNum))
#     connection.commit()
#     askAddAnotherRide = input("Would you like to add another ride? [Y/N] ")
#     if askAddAnotherRide.upper() == Y:
#         offer(cursor, connection, email)
#     return #???????


# def checkValidDate(date): #fix to check if date is in future
#     date = date
#     date1 = date.split('-')
#     #print(date1)
#     if (len(date1) != 3) or (date[4] != '-') or (date[7] != '-'):
#         return False
#     else:
#         return True

def getLocation(cursor, conn, email):
    while True:
        location = input().lower() # OR TYPE IN EXIT TO GO BACK?
        # TODO: CHECK TO MAKE SURE LOCATION CODE INPUT IS CORRECT
        # if (location == 'EXIT'):
        #     break

        cursor.execute('''SELECT city, prov FROM locations WHERE lcode = ? ;''', (location,))
        found = cursor.fetchone()
        if found != None:
            return location
        else:
            keyword = '%' + location + '%'
            cursor.execute('''SELECT * FROM locations WHERE (city LIKE ? OR prov LIKE ? OR address LIKE ?);''', (keyword, keyword, keyword))
            locationList = cursor.fetchall()
            print("Locations with similar keyword(s): ")
            print("Code | City | Province | Address")

            locationSet = set()
            for location in locationList:
                # NEED 5 PER PAGE FILTER HERE @JACKIE
                if location[0] not in locationSet:
                    locationSet.add(str(location[0]))

                print(str(location[0]) + " | " + str(location[1]) + " | " + str(location[2]) + " | " + str(location[3]))

            selection = input("Select one of the above locations by entering the appropriate location code: ").lower()
            if selection not in locationSet:
                selection = input("Try again and enter an appropriate location code: ").lower()

            return selection



# def getLoc(cursor, conn, email): #fix so can find location if keyword not a lcode
#     location = input("Enter a location code or keyword to search: ")
#     cursor.execute("SELECT city, prov from locations where ? = lcode", (location.lower(),))
#     location = '%' + location.lower() + '%'
#     found = cursor.fetchone()
#     if found != None:
#         confirm = input("Location " + found[0] + " " + found[1] + ". Is this correct? [Y/N]")
#         if confirm.upper() == 'Y':
#             return location.lower()
#         else:
#         	return getLoc(cursor, conn, email)
#     else:
#         cursor.execute("SELECT * from locations where (city like ? or prov like ? or address like ?) ", (location, location, location))
#         locSet = cursor.fetchall()
#         count = 0
#         loops = 0
#         for location in locSet:
#             print("Option " + str(count + 1) + ': ' + location[1] + " " + location[2] + " " + location[3])
#             if count == 4 or location == locSet[len(locSet) - 1]:
#                 choice = input("Select one of these locations? (Enter option # or press enter to see more)")
#                 if choice == '':
#                     count = -1
#                     loops +=1
#                 else:
#                     try:
#                         choice = int(choice)
#                         return locSet[(loops * 4) + (choice - 1)][0]
#                     except ValueError:
#                         print("Invalid option. Please retry search.")
#                         return getLoc(cursor, conn, email)
#                 count += 1
#         print("Location not found. Please try another location code or keyword")
#         return getLoc(cursor, conn, email)

def searchRides(cursor, conn, email):
    pass
