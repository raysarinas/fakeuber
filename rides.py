# 1 - OFFER A RIDE
# 2 - SEARCH FOR RIDES
import sqlite3
import main, login, re
import time, datetime
from clear import clear

def offerRide(cursor, conn, email):
    print('Offer a ride by entering the following information: ')

    while True:
        date = input('Ride Date (YYYY-MM-DD)? ')
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
        while seats.isdigit() == False:
            seats = input("Invalid input. Enter a numerical amount: ")
        seats = int(seats)

        price = input("What is the price per seat? ")
        while price.isdigit() == False:
            price = input("Invalid input. Enter a numerical amount: ")
        price = int(price)

        luggage = input("Enter luggage description: ")
        while len(luggage) > 10:
            luggage = input("Desciption too long. Enter a shorter description: ")

        # CHECK LOCATION STUFFFFFFF
        source = input("Enter a pickup location code or keyword: ")
        source = getLocation2(cursor, source) #getLoc(cursor, conn, email).replace("%", "")
        dest = input("Enter a dropoff location code or keyword: ")
        dest = getLocation2(cursor, dest) #getLoc(cursor, conn, email).replace("%", "")

        askCarNum = input("Would you like to add a car number? Enter 'Y' if yes. Otherwise, enter anything else: ")
        while askCarNum.lower() == 'y':
            cno = input("Enter your car number: ")
            while cno.isdigit() == False:
                cno = input("That's not a number try again: ")
            cno = int(cno)
            #print("input cno: " + str(type(cno)) + " " + str(cno))
            cursor.execute("SELECT cno FROM cars WHERE owner = ? AND cno = ?;", (email, cno))

            cnoFetched = cursor.fetchone()
            #print("fetched cno: " + str(type(cnoFetched)) + " " + str(cnoFetched))
            if (cnoFetched == None):
                cnoFetched = input("Car is not registered with you; try again by entering 'Y', otherwise enter anything else: ")
            else:
                cno = cnoFetched[0]
                print("Car number registered!")
                break

        rno = getRNO(cursor, conn, email)
        #TODO: FIX: ERROR WHEN BLANK INPUT
        cursor.execute('''INSERT INTO rides
                VALUES (?,?,?,?,?,?,?,?,?);''', (rno, price, date, seats, luggage, source, dest, email, cno))
        conn.commit()

        getEnroutes(cursor, conn, rno)

        # @JUJU PLZ CHECK IF THESE VALUES ARE RIGHT LIKE rno ?????
        # IDK IM CONFUSED BUT IT SHOULD WORK
        # UNCOMMENT THE NEXT 2 LINES
        # cursor.execute(''' SELECT * FROM enroute;''')
        # print(cursor.fetchall())
        clear()
        print('Ride Offering Posted!')

        break

def getEnroutes(cursor, conn, rno):
    enroutes = []
    askEnroutes = input("Would you like to add any enroute locations? Enter 'Y' if yes. Otherwise, enter anything else: ")

    if askEnroutes == 'y':
        while True:
            location = input("Enter an enroute location code or keyword: ")
            enroutes.append(getLocation(cursor, location))
            askAgain = input("If you would like to add another enroute location, Enter 'Y'. Otherwise, enter anything else: ")
            if askAgain != 'y':
                break

    enrouteLen = len(enroutes)
    if enrouteLen > 0:
        for i in range(enrouteLen):
            cursor.execute(''' INSERT INTO enroute VALUES (?, ?);''', (rno, enroutes[i]))
            conn.commit()

def getCarNum(cursor, conn, email):
    carNum = input("Enter car number: ")
    while carNum.isdigit() == False:
        carNum = getCarNum(cursor, conn, email)

    carNum = int(carNum)

    cursor.execute("SELECT cno from cars where owner = ? and cno = ?", (email, carNum))
    cnoFetched = cursor.fetchone()[0]
    print(type(cnoFetched))
    print(" ------ TEST ----- " + str(cnoFetched))
    ''' OPTION TO SAY CANT OFFER A RIDE IF HAVE NO CAR ???????????
        CANT ADD A CNO BECAUSE CANT OFFER A RIDE IF NO CAR AND IF NO CAR CANT ADD CNO
        EGOUBHDGSNAFML;SDNGPIFARWKFEGWRHETOJW[ADKS'F;ET]WR[GHETRW]
    '''

    if cursor.fetchone() == None: # or cnoFetched != carNum:
        askAgain = input("Car is not registered with you, please try again by entering 'Y'. Otherwise, no: ")
        if askAgain.lower() == 'y':
            getCarNum(cursor, conn, email)
        else:
            return None
    else:
        return cnoFetched

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

def getLocation2(cursor, location):
    while True:
        location = location.lower()
        #location = input().lower() # OR TYPE IN EXIT TO GO BACK?
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
            cursor.execute('''SELECT * FROM locations WHERE (lcode LIKE ? OR city LIKE ? OR prov LIKE ? OR address LIKE ?);''', (keyword, keyword, keyword, keyword))
            locationList = cursor.fetchall()
            print("Locations with similar keyword: ")
            print("Code | City | Province | Address")
            locationSet = set()
            for location in locationList:
                # NEED 5 PER PAGE FILTER HERE @JACKIE
                if location[0] not in locationSet:
                    locationSet.add(str(location[0]))

            locList = locationList
            locListLen = len(locList)
            counter = 0
            gotLocation = 0
            exitWanted = 0
            while True:
                if counter < locListLen:
                    location = locList[counter]
                    print(str(location[0]) + " | " + str(location[1]) + " | " + str(location[2]) + " | " + str(location[3]))
                    counter += 1

                if counter % 5 == 0 or counter == locListLen:
                    if counter == locListLen:
                        print('End of the list')
                    print("Select one of the above locations by entering the appropriate location code")
                    selection = input("Otherwise, anything else will show the next 5: ").lower()
                    if selection not in locationSet:
                        # selection = input("Try again and enter an appropriate location code: ").lower()
                        print('Next 5')
                        continue

                    return selection


def getLocation(cursor, location):
    while True:
        location = location.lower()
        #location = input().lower() # OR TYPE IN EXIT TO GO BACK?
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
            cursor.execute('''SELECT * FROM locations WHERE (lcode LIKE ? OR city LIKE ? OR prov LIKE ? OR address LIKE ?);''', (keyword, keyword, keyword, keyword))
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

def keyWordLocations(cursor, keywords):
    locationSet = set()

    for word in keywords:
        word = '%' + word.lower() + '%'
        cursor.execute('''SELECT * FROM locations WHERE (lcode LIKE ? OR city LIKE ? OR prov LIKE ? OR address LIKE ?);''', (word, word, word, word))
        locationList = cursor.fetchall()

        for location in locationList:
            # MAYBE NEED 5 PER PAGE FILTER HERE @JACKIE
            if location[0] not in locationSet:
                locationSet.add(str(location[0]))
            # print(str(location[0]) + " | " + str(location[1]) + " | " + str(location[2]) + " | " + str(location[3]))

    return locationSet

        # selection = input("Select one of the above locations by entering the appropriate location code: ").lower()
        # if selection not in locationSet:
        #     selection = input("Try again and enter an appropriate location code: ").lower()
        #
        # return selection


def searchRides(cursor, conn, email):
    while True:
        keyIn = input("Enter up to 3 keywords to search rides: ")
        keywords = keyIn.split()

        while (len(keywords) > 3 or len(keywords) < 1):

            less = input("Enter different ammount of keywords. Try again: ")
            keywords = less.split()

        locationSet = keyWordLocations(cursor, keywords)
        locList = list(locationSet)

        # CHECK IF LIST IS EMPTY
        if len(locList) == 0:
            print("There are no rides associated with the provided keywords.")
            break
        # ELSE IF NOT EMPTY THEN DO SHIT
        else:
            rnoSet = set()
            for location in locList:
                # QUERY SO THAT
                cursor.execute(''' SELECT DISTINCT rides.rno
                                    FROM rides, enroute
                                    WHERE src = ? OR dst = ?
                                    OR (enroute.lcode = ? AND rides.rno = enroute.rno);''', (location, location, location))
                rnoFetched = cursor.fetchall()

                for tup in rnoFetched:
                    if tup[0] not in rnoSet:
                        rnoSet.add(tup[0])

        rnoList = sorted(rnoSet)
        outputList = []

        for rno in rnoList:
            cursor.execute(''' SELECT DISTINCT rides.*, cars.*
                                FROM rides
                                LEFT JOIN cars on rides.cno = cars.cno
                                WHERE rno = ?''', (rno,))
            outputList.append(cursor.fetchone())

        print("Rides with matching to entered keywords: ")
        print("ID | Price | Date | Seats | Luggage Description | Source | Destination | Driver | CarNum | Make | Model | Year | Seats | Owner")

        outputListLen = len(outputList)
        counter = 0
        sentMessage = 0
        exitWanted = 0
        while True:
            if counter < outputListLen:
                row = outputList[counter]
                print(str(row[0]) + " | " + str(row[1]) + " | " + str(row[2]) + " | " + str(row[3]) + " | ", end='')
                print(str(row[4]) + " | " + str(row[5]) + " | " + str(row[6]) + " | " + str(row[7]) + " | ", end='')
                print(str(row[8]) + " | " + str(row[9]) + " | " + str(row[10]) + " | " + str(row[11]) + " | ", end='')
                print(str(row[12]) + " | " + str(row[13]))
                counter += 1

            if counter % 5 == 0 or counter == outputListLen:
                if counter == outputListLen:
                    print('End of the list')

                print("If you wish to message a poster about a ride, enter the ID number of the ride. ")
                rnoInput = input("enter 'EXIT' to exit the search. Otherwise, enter anything else to see next 5: ").upper()

                if rnoInput.isdigit() == False:
                    if rnoInput == 'EXIT':
                        exitWanted = 1
                        break
                    else:
                        continue
                else:
                    rnoInput = int(rnoInput)

                    cursor.execute(''' SELECT driver FROM rides WHERE rno = ?;''', (rnoInput,))
                    driver = cursor.fetchone()[0]
                    print(driver)
                    messageDriver(cursor, conn, email, rnoInput, driver)
                    sentMessage = 1
                    break
        if sentMessage == 1 or exitWanted == 1:
            break
        # JUJU IMPLEMENT ASKING WHAT TO DO NEXT

def messageDriver(cursor, conn, email, rno, driver):
    clear()
    while True:
        message = input("Enter the message you wish to send to " + str(driver) + " about ride with RNO #" + str(rno) + ": ")
        cursor.execute(''' INSERT INTO inbox VALUES (?,datetime('now'),?,?,?,'n');''', (driver, email, message, rno))
        conn.commit()
        print('Message sent!')
        break
