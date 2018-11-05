# 1 - OFFER A RIDE
# 2 - SEARCH FOR RIDES
import sqlite3
import main, login, re
import time, datetime
from clear import clear

def offerRide(cursor, conn, email):
    # allows user to offer a ride by entering inputs corresponding to specification
    print('Offer a ride by entering the following information: ')

    while True:
        # take in date input and check if it is in the correct format
        date = input('Ride Date (YYYY-MM-DD)? ')
        dateCheck = re.match("^[\d]{4}\\-[\d]{2}\\-[\d]{2}$", date)
        if dateCheck is None:
            print('Invalid Date. Try Again')
            continue
        else: # CONVERT TO DATE TYPE
            year, month, day = map(int, date.split('-'))
            date = datetime.date(year, month, day)

        # get various inputs while checking if the inputs are correct
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

        # parse and get locations based on user input
        source = None
        while source is None:
            source = input("Enter a pickup location code or keyword: ")
            source = getLocation(cursor, source)

        dest = None
        while dest is None:
            dest = input("Enter a dropoff location code or keyword: ")
            dest = getLocation(cursor, dest)

        # ask if user wants to add a car number
        askCarNum = input("Would you like to add a car number? Enter 'Y' if yes. Otherwise, enter anything else: ")

        # find out if user owns a car or is associated with a car
        # if no cars registered with user, then jump out and dont add a car number
        cursor.execute("SELECT cno FROM cars WHERE owner = ?;", (email,))
        if not cursor.fetchall():
            print("You don't have any cars registered with you! So bye")
            cno = None
        else:
            # otherwise, if there is a car number registered with the user, find that car number
            # and use it to be included in following query(ies)
            while askCarNum.lower() == 'y':
                cno = input("Enter your car number: ")
                while cno.isdigit() == False:
                    cno = input("That's not a number try again: ")
                cno = int(cno)
                cursor.execute("SELECT cno FROM cars WHERE owner = ? AND cno = ?;", (email, cno))

                cnoFetched = cursor.fetchone()
                if (cnoFetched == None):
                    cnoFetched = input("Car is not registered with you; try again by entering 'Y', otherwise enter anything else: ")
                else:
                    cno = cnoFetched[0]
                    print("Car number registered!")
                    break

        # get the ride number or create a new one by calling getRNO
        rno = getRNO(cursor, conn, email)
        # ask if user wants to add enroute locations
        #getEnroutes(cursor, conn, rno)
        # insert the input values into the rides table and commit to database
        cursor.execute('''INSERT INTO rides
                VALUES (?,?,?,?,?,?,?,?,?);''', (rno, price, date, seats, luggage, source, dest, email, cno))
        conn.commit()

        getEnroutes(cursor, conn, rno)
        clear()
        print('Ride Offering Posted!')

        break

def getEnroutes(cursor, conn, rno):
    # get enroute locations by prompting user to ask if they want to add enroute locations
    enroutes = [] # initialize empty list to hold enroutes
    askEnroutes = input("Would you like to add any enroute locations? Enter 'Y' if yes. Otherwise, enter anything else: ")

    if askEnroutes == 'y':
        while True:
            # parse locations similar to when offering a ride
            location = input("Enter an enroute location code or keyword: ")
            enroutes.append(getLocation(cursor, location))
            # ask again if more than one enroute is wanted to be added
            askAgain = input("If you would like to add another enroute location, Enter 'Y'. Otherwise, enter anything else: ")
            if askAgain != 'y':
                break

    # get length of enroutes, and if the list is not empty, commit it and add to database
    print(enroutes)
    enrouteLen = len(enroutes)
    if enrouteLen > 0:
        for i in range(enrouteLen):
            cursor.execute(''' INSERT INTO enroute VALUES (?, ?);''', (rno, enroutes[i]))
            conn.commit()


def getRNO(cursor, conn, email):
    # create a new RNO for new rides to be offered by taking maximum number already
    # in table and then adding 1 so RNO is UNIQUE
    cursor.execute(''' SELECT MAX(rides.rno) FROM rides;''')
    last = cursor.fetchall()
    if last == None:
        return 1
    rno = int(last[0][0])+ 1
    return rno

def getLocation(cursor, location):
    # get a location for user to pick from
    # either user enters a correct location code or a keyword and then
    # if a keyword is entered, will display every associated location with
    # said keyword
    while True:
        location = location.lower() # make all lowercase
        cursor.execute('''SELECT city, prov FROM locations WHERE lcode = ? ;''', (location,))
        found = cursor.fetchone()

        if found != None:
            # if find a matching location code, then return it
            return location
        else:
            # otherwise, look for a keyword
            keyword = '%' + location + '%'
            cursor.execute('''SELECT * FROM locations WHERE (lcode LIKE ? OR city LIKE ? OR prov LIKE ? OR address LIKE ?);''', (keyword, keyword, keyword, keyword))
            locationList = cursor.fetchall()
            print("Locations with similar keyword: ")
            print("Code | City | Province | Address")

            # create a set of the locations
            # add into set if not there yet
            locationSet = set()
            for location in locationList:
                if location[0] not in locationSet:
                    locationSet.add(str(location[0]))

            if not locationSet:
                print('No locations found with that keyword. Try again. ')
                return None

            # local variables to keep track of 5 per page thing
            # and also what has been printed
            locList = locationList
            locListLen = len(locList)
            counter = 0
            gotLocation = 0
            exitWanted = 0

            while True:
                if counter < locListLen:
                    location = locList[counter] # Get the current index of the list
                    # display locations onto screen
                    print(str(location[0]) + " | " + str(location[1]) + " | " + str(location[2]) + " | " + str(location[3]))
                    counter += 1
                # If we have print 5 or at the end of list notify
                if counter % 5 == 0 or counter == locListLen:
                    if counter == locListLen:
                        print('End of the list')
                    print("Select one of the above locations by entering the appropriate location code")
                    selection = input("Otherwise, anything else will show the next 5: ").lower()
                    if selection not in locationSet: # See next 5
                        print('Next 5')
                        continue

                    return selection



def keyWordLocations(cursor, keywords):
    # specifically for when searching rides, if multiple keywords are entered,
    # then for each keyword, find a location that may be asscoiated and put it
    # into a set and then return that set of locations to avoid duplicates
    # and for use later in searchRides function
    locationSet = set()

    for word in keywords:
        word = '%' + word.lower() + '%'
        cursor.execute('''SELECT * FROM locations WHERE (lcode LIKE ? OR city LIKE ? OR prov LIKE ? OR address LIKE ?);''', (word, word, word, word))
        locationList = cursor.fetchall()

        for location in locationList:
            if location[0] not in locationSet:
                locationSet.add(str(location[0]))

    return locationSet

def searchRides(cursor, conn, email):
    # search for rides functionality. user can enter up to 3 keywords
    while True:
        keyIn = input("Enter up to 3 keywords to search rides: ")
        keywords = keyIn.split()

        # if no keywords or too many, prompt to ask again
        while (len(keywords) > 3 or len(keywords) < 1):

            less = input("Enter different ammount of keywords. Try again: ")
            keywords = less.split()

        # obtain set of locations based on keywords and then
        # put that into a list so easier to iterate through
        locationSet = keyWordLocations(cursor, keywords)
        locList = list(locationSet)

        # CHECK IF LIST IS EMPTY
        if len(locList) == 0:
            print("There are no rides associated with the provided keywords.")
            break
        else:
            # else for each location, get associated rno's and put into a set
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

        # sort the set of rno's and initialize a list for outputs
        rnoList = sorted(rnoSet)
        outputList = []

        for rno in rnoList:
            # get every rno associated with ride and left join it
            # with cars table so can get all car data as well
            # append each selection from query into output list
            cursor.execute(''' SELECT DISTINCT rides.*, cars.*
                                FROM rides
                                LEFT JOIN cars on rides.cno = cars.cno
                                WHERE rno = ?''', (rno,))
            outputList.append(cursor.fetchone())

        # display the output list
        print("Rides with matching to entered keywords: ")
        print("ID | Price | Date | Seats | Luggage Description | Source | Destination | Driver | CarNum | Make | Model | Year | Seats | Owner")

        outputListLen = len(outputList)
        counter = 0
        sentMessage = 0
        exitWanted = 0
        while True:
            if counter < outputListLen:
                row = outputList[counter] # Show current index of our list
                print(str(row[0]) + " | " + str(row[1]) + " | " + str(row[2]) + " | " + str(row[3]) + " | ", end='')
                print(str(row[4]) + " | " + str(row[5]) + " | " + str(row[6]) + " | " + str(row[7]) + " | ", end='')
                print(str(row[8]) + " | " + str(row[9]) + " | " + str(row[10]) + " | " + str(row[11]) + " | ", end='')
                print(str(row[12]) + " | " + str(row[13]))
                counter += 1
            # Check if 5th index or end of the list
            if counter % 5 == 0 or counter == outputListLen:
                if counter == outputListLen:
                    print('End of the list')

                print("If you wish to message a poster about a ride, enter the ID number of the ride. ")
                rnoInput = input("enter 'EXIT' to exit the search. Otherwise, enter anything else to see next 5: ").upper()
                # Check command/what to do if string was entered
                if rnoInput.isdigit() == False:
                    if rnoInput == 'EXIT':
                        exitWanted = 1
                        break
                    else:
                        continue
                else:
                    rnoInput = int(rnoInput)
                    # Get the email of the driver for the ride
                    cursor.execute(''' SELECT driver FROM rides WHERE rno = ?;''', (rnoInput,))
                    driver = cursor.fetchone()[0]
                    # Send a message to the driver
                    messageDriver(cursor, conn, email, rnoInput, driver)
                    sentMessage = 1
                    break
        # Break if a message was sent or we want to exit
        if sentMessage == 1 or exitWanted == 1:
            break

def messageDriver(cursor, conn, email, rno, driver):
    # message the driver
    clear()
    while True:
        # ask what message is to be sent and then commit it i guess
        message = input("Enter the message you wish to send to " + str(driver) + " about ride with RNO #" + str(rno) + ": ")
        cursor.execute(''' INSERT INTO inbox VALUES (?,datetime('now'),?,?,?,'n');''', (driver, email, message, rno))
        conn.commit()
        print('Message sent!')
        break
