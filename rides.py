# 1 - OFFER A RIDE
# 2 - SEARCH FOR RIDES
import sqlite3
import main, login
#import time, datetime

def offerRide(cursor, conn, email):
    date = input("Date of the ride: (YYYY-MM-DD): ")
    if not checkValidDate(date):
        print("Invalid format: PLease try again (YYYY-MM-DD)")
        offerRide(cursor, conn, email)

    numSeats = input("Enter number of seats: ")
    validNumSeats(numSeats)

    seatPrice = input("Enter price per seat: ")
    validSeatPrice(seatPrice)

    luggage = input("Enter luggage description: ") #fix luggage desc?????
    print("Source Location")
    sourceLoc = getLoc(cursor, conn, email)
    print("Destination Location")
    destLoc = getLoc(cursor, conn, email)
    carNum = 'NULL' #if did not want to enter a car num
    askCarNum = input("Would you like to add a car number? [Y/N]")
    if askCarNum.upper() == 'Y':
        carNum = getCarNum(cursor, conn, email)

    # elif askCarNum.upper() == 'N':
    #     enrouteSet = []
    #     askEnroute = input("Would you like to add an enroute location? [Y/N]")
    #     if askEnroute.upper() == 'Y':
    #         addEnroute = getLoc(cursor, conn)
    #         enrouteSet.append(addEnroute)
    #         askEnrouteAgain = input ("Would you like to add another enroute location? [Y/N] ")

    #rideNum = getRideNum(cursor, conn)

    enrouteSet = []
    askEnroute = input("Would you like to add an enroute location? [Y/N]")
    if askEnroute.upper() == 'Y':
        addEnroute = getLoc(cursor, conn, email)
        enrouteSet.append(addEnroute)
        askEnrouteAgain = input ("Would you like to add another enroute location? [Y/N] ")
        #if askEnrouteAgain.upper() == 'Y':
            #######fix this move this somewhere???
    # elif askEnroute.upper() == 'N':
    #     return
    assignRideNum = getRideNum(cursor, conn, email)
    if len(enrouteSet) != 0:
        for loc in enrouteSet:
            cursor.execute("INSERT INTO enroute values (?, ?)", (assignRideNum, loc))
            connection.commit()
    cursor.execute("INSERT INTO rides values (?, ?, ?, ?, ?, ?, ?, ?, ?)", (assignRideNum, seatPrice, date, numSeats, luggage, sourceLoc, destLoc, email, carNum))
    connection.commit()
    askAddAnotherRide = input("Would you like to add another ride? [Y/N] ")
    if askAddAnotherRide.upper() == Y:
        offer(cursor, connection, email)
    return #???????


def checkValidDate(date): #fix to check if date is in future
    date = date
    date1 = date.split('-')
    #print(date1)
    if (len(date1) != 3) or (date[4] != '-') or (date[7] != '-'):
        return False
    else:
        return True

def validNumSeats(numSeats):
    if not numSeats.isdigit():
        print("Invalid number of seats, please enter a number")
        numSeats = input("Enter number of seats: ")
        validNumSeats(numSeats)
        return False
    else:
        return True

def validSeatPrice(seatPrice):
    if not seatPrice.isdigit():
        print("Invalid price of seats, please enter a number")
        seatPrice = input("Enter number of seats: ")
        validSeatPrice(seatPrice)
        return False
    else:
        return True

def getLoc(cursor, conn, email): #fix so can find location if keyword not a lcode
    location = input("Enter a location code or keyword to search: ")
    cursor.execute("SELECT city, prov from locations where ? = lcode", (location.lower(),))
    location = '%' + location.lower() + '%'
    found = cursor.fetchone()
    if found != None:
        confirm = input("Location " + found[0] + " " + found[1] + ". Is this correct? [Y/N]")
        if confirm.upper() == 'Y':
            return location.lower()
        else:
        	return getLoc(cursor, conn, email)
    else:
        cursor.execute("SELECT * from locations where (city like ? or prov like ? or address like ?) ", (location, location, location))
        locSet = cursor.fetchall()
        count = 0
        loops = 0
        for location in locSet:
            print("Option " + str(count + 1) + ': ' + location[1] + " " + location[2] + " " + location[3])
            if count == 4 or location == locSet[len(locSet) - 1]:
                choice = input("Select one of these locations? (Enter option # or press enter to see more)")
                if choice == '':
                    count = -1
                    loops +=1
                else:
                    try:
                        choice = int(choice)
                        return locSet[(loops * 4) + (choice - 1)][0]
                    except ValueError:
                        print("Invalid option. Please retry search.")
                        return getLoc(cursor, conn, email)
                count += 1
        print("Location not found. Please try another location code or keyword")
        return getLoc(cursor, conn, email)


def getCarNum(cursor, conn, email):
    carNum = input("Enter car number: ")
    cursor.execute("SELECT cno from cars where owner = ? and cno = ?", (email, carNum))
    if cursor.fetchone() != None:
        return carNum
    else:
        print("Car is not registered with you, please try again")
        getCarNum(cursor, conn, email)



def getRideNum(cursor, conn, email):
    cursor.execute("SELECT max(rno) from rides")
    last = cursor.fetchone()
    if last == None:
        return 1
    rno = last[0] + 1
    return rno

def searchRides(cursor, conn, email):
    pass
