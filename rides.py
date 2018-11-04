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
        print("Enter a pickup location code or keyword: ", end='')
        source = getLocation(cursor) #getLoc(cursor, conn, email).replace("%", "")
        print("Enter a dropoff location code or keyword: ", end='')
        dest = getLocation(cursor) #getLoc(cursor, conn, email).replace("%", "")

        print("Would you like to add a car number? Enter 'Y' if yes. Otherwise, enter anything else. ", end='')
        while True:
            cno = None # OR SHOULD THIS BE NULL????? # if did not want to enter a car num
            askCarNum = input()
            if askCarNum.lower() == 'y':
                cno = getCarNum(cursor, conn, email)
            else:
                break

        enroutes = []
        askEnroutes = input("Would you like to add any enroute locations? Enter 'Y' if yes. Otherwise, enter anything else: ")

        if askEnroutes == 'y':
            while True:
                print("Enter an enroute location code or keyword: ", end='')
                enroutes.append(getLocation(cursor))
                askAgain = input("If you would like to add another enroute location, Enter 'Y'. Otherwise, enter anything else: ")
                if askAgain != 'y':
                    break

        rno = getRNO(cursor, conn, email)
        cursor.execute('''INSERT INTO rides
                VALUES (?,?,?,?,?,?,?,?,?);''', (rno, price, date, seats, luggage, source, dest, email, cno))
        conn.commit()

        enrouteLen = len(enroutes)
        if enrouteLen > 0:
            for i in range(enrouteLen):
                cursor.execute(''' INSERT INTO enroute VALUES (?, ?);''', (rno, enroutes[i]))
                conn.commit()

        # @JUJU PLZ CHECK IF THESE VALUES ARE RIGHT LIKE rno ?????
        # IDK IM CONFUSED BUT IT SHOULD WORK
        # UNCOMMENT THE NEXT 2 LINES
        # cursor.execute(''' SELECT * FROM enroute;''')
        # print(cursor.fetchall())

        print('Ride Offering Posted!')

        break


def getCarNum(cursor, conn, email):
    carNum = input("Enter car number: ")
    while carNum.isdigit() == False:
        carNum = input("Incorrect input, please enter a number: ")
    carNum = int(carNum)
    cursor.execute("SELECT cno from cars where owner = ? and cno = ?", (email, carNum))
    if cursor.fetchone() == None or cursor.fetchone()[0] != carNum:
        print("Car is not registered with you, please try again by entering 'Y'. Otherwise, no: ", end='')
        carNum = None

def getRNO(cursor, conn, email):
    cursor.execute(''' SELECT MAX(rides.rno) FROM rides;''')
    last = cursor.fetchall()
    if last == None:
        return 1
    rno = int(last[0][0])+ 1
    return rno

# def checkValidDate(date): #fix to check if date is in future
#     date = date
#     date1 = date.split('-')
#     #print(date1)
#     if (len(date1) != 3) or (date[4] != '-') or (date[7] != '-'):
#         return False
#     else:
#         return True

def getLocation(cursor):
    while True:
        location = input().lower() # OR TYPE IN EXIT TO GO BACK?
        # TODO: CHECK TO MAKE SURE LOCATION CODE INPUT IS CORRECT
        # LOCATION CODE SHOULD HAVE MAX LEN 5 --- Char(5)???
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
            print("Locations with similar keyword: ")
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

def searchRides(cursor, conn, email):

    pass
    while True:
        keyIn = input("Enter up to 3 keywords to search rides: ")
        keywords = keyIn.split()

        if ((len(keywords) > 3) or (len(keywords) == 0)):
            print("Too many or too little keywords! Try again. ")
            continue

        # get the ride requests with the inputted pickup location
        # FIX THIS QUERY WHEN ACTUALLY NOT DYING
        cursor.execute(''' SELECT DISTINCT requests.rid, requests.email, requests.rdate, requests.pickup,
                            requests.dropoff, requests.amount
                            FROM locations, requests
                            WHERE lcode = ? AND pickup = lcode;''', (filter,))
        filteredRequests = cursor.fetchall()
        numRequests = len(filteredRequests)

        # TODO:NEED TO FILTER OUT ONLY 5 PER PAGE????
        if (numRequests == 0):
            print("There are no ride requests with the given pickup location.")
            break

        else:
            print("Ride Requests with Pickup Location: " + filter)
            print("ID | Date | Pickup | Dropoff | Amount | Poster")
            for request in filteredRequests:
                print(str(request[0]) + " | " + str(request[2]) + " | " + str(request[3]) + " | " + str(request[4]) + " | " + str(request[5]) + " | " + str(request[1]))
            print("\n")

            print("If you wish to message a poster, enter the email of the poster you wish to message.")
            emailMember = input("Otherwise, enter anything else: ")
            emailCheck = re.match("^[_\d\w]+\\@[_\d\w]+\\.[_\d\w]+$", emailMember)

            if emailCheck is None:
                print('Invalid email. Try again?')
                continue
            else:
                #break
                messagePoster(cursor, conn, email, emailMember)
                # RIGHT HERE SHOULD BE ABLE TO MESSAGE MEMBER
