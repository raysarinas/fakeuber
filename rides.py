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

    sourceLoc = getLoc(cursor, conn, email)
    destLoc = getLoc(cursor, conn, email)
    askCarNum = input("Would you like to add a car number? [Y/N]")
    if askCarNum.upper() == 'Y':
        carNum = getCarNum(cursor, conn, email)
        
    elif askCarNum.upper() == 'N':
        enrouteSet = []
        askEnroute = input("Would you like to add an enroute location? [Y/N]")
        if askEnroute.upper() == 'Y':
            addEnroute = getLoc(cursor, conn)
            enrouteSet.append(addEnroute)
            askEnrouteAgain = input ("Would you like to add another enroute location? [Y/N] ")

    rideNum = getRideNum(cursor, conn)

    # enrouteSet = []
    # askEnroute = input("Would you like to add an enroute location? [Y/N]")
    # if askEnroute.upper() == 'Y':
    #     addEnroute = getLoc(cursor, conn)
    #     enrouteSet.append(addEnroute)
    #     askEnrouteAgain = input ("Would you like to add another enroute location? [Y/N] ")
    #     #if askEnrouteAgain.upper() == 'Y':
            ########fix this move this somewhere???
    # elif askEnroute.upper() == 'N':
    #     return

    if len(enrouteSet) != 0:
        for loc in enrouteSet:
            cursor.execute("INSERT INTO enroute values (?, ?)", (rideNum, loc))
            connection.commit()
    cursor.execute("INSERT INTO rides values (?, ?, ?, ?, ?, ?, ?, ?, ?)", (rideNum, seatPrice, date, numSeats, luggage, sourceLoc, destLoc, carNum))
    connection.commit()
    askAddAnotherRide = input("Would you like to add another ride? [Y/N] ")
    if askAddAnotherRide.upper() == Y:
        offer(cursor, connection, email)
    return


def checkValidDate(date):
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

def getLoc(cursor, conn, email):
    #finshhhhhhhhhh#########
    location = input("Enter a location code or keyword to search: ")
    cursor.execute("SELECT city, prov from locations where ? = lcode", (location.lower(),))



def getCarNum(cursor, conn, email):
    carNum = input("Enter car number: ")
    cursor.execute("SELECT cno from cars where owner = ? and cno = ?", (email, carNum))
    if cursor.fetchone() != None:
        return carNum
    else:
        print("Car is not registered with you, please try again")
        getCarNum(cursor, conn, email)



#def getRideNum(cursor, conn, email)
    ###finsih##########

#def searchRides(cursor, conn, email)
    ####finish#########
