# 1 - OFFER A RIDE
# 2 - SEARCH FOR RIDES
import sqlite3
import main, login
#import time, datetime

def offerRide(cursor, conn):
    date = input("date ride be on (YYYY-MM-DD): ")
    if not checkValidDate(date):
        print("Invalid format: PLease try again (YYYY-MM-DD)")
        offerRide(cursor, conn)

    numSeats = input("Enter number of seats: ")
    seatPrice = input("Enter price per seat: ")
    luggage = input("Enter luggage description: ")
    sourceLoc = getLoc(cursor, conn)
    destLoc = getLoc(cursor, conn)
    askCarNum = input("Would you like to add a car number? [Y/N]")
    if askCarNum.upper() == 'Y':
        carNum = getCarNum(cursor, conn)
        ########get car

    rideNum = getRideNum(cursor, conn)
    enrouteSet = []
    askEnroute = input("Would you like to add an enroute location? [Y/N]")
    if askEnroute.upper() == 'Y':
        addEnroute = getLoc(cursor, conn)
        enrouteSet.append(addEnroute)
        askEnrouteAgain = input ("Would you like to add another enroute location? [Y/N] ")
        if askEnrouteAgain.upper() == 'Y':
            #########

    if len(enrouteSet) != 0:
        for loc in enrouteSet:
            cursor.execute("INSERT INTO enroute values (?, ?)", (rideNum, loc))
			connection.commit()
    cursor.execute("INSERT INTO rides values (?, ?, ?, ?, ?, ?, ?, ?, ?)", (rideNum, seatPrice, date, numSeats, luggage, sourceLoc, destLoc, carNum))
	connection.commit()



def checkValidDate(date):
    date = date
    date1 = date.split('-')
    if (len(date1) != 3) or (date[4] != '-') or (date[7] != '-'):
        return False

def getCarNum(cursor, conn):
    #get email
    carNum = input("Enter car number: ")
    cursor.execute("SELECT cno from cars where owner = ? and cno = ?", (email, car))
	if cursor.fetchone() != None:
		return car
	cont = input("That car does not belong to you - would you like to enter another (Y/N)? ")
	if cont.upper() == 'Y':
		return get_car(cursor, connection, email)
	else:
		return None
