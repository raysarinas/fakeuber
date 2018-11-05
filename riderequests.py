# 4 - POST RIDE REQUESTS
# 5 - SEARCH AND DELETE RIDE requests

import re, rides, datetime, time
from os import system, name
from clear import clear

def getReqID(cursor, conn, email):
    # create a new request ID for a new ride request
    # works similar to getting a unique RNO
    #
    cursor.execute(''' SELECT MAX(requests.rid) FROM requests;''')
    last = cursor.fetchall()
    if last == None:
        return 1
    rid = int(last[0][0])+ 1
    return rid



def postRequest(cursor, conn, email):
    # allows user/member to post a ride request by entering inputs
    # corresponding to specification
    clear() # clear screen

    print('Post a Ride Request by entering the following information: ')
    while True:
        # take in date input and check if correct formatting
        date = input('Ride Date (YYYY-MM-DD)? ')
        dateCheck = re.match("^[\d]{4}\\-[\d]{2}\\-[\d]{2}$", date)
        if dateCheck is None:
            print('Invalid Date. Try Again')
            continue
        else: # CONVERT TO DATE TYPE
            year, month, day = map(int, date.split('-'))
            date = datetime.date(year, month, day)

        pickup = None
        while pickup is None:
            pickup = input("Enter a pickup location code or keyword: ")
            pickup = rides.getLocation(cursor, pickup)

        dropoff = None
        while dropoff is None:
            dropoff = input("Enter a dropoff location code or keyword: ")
            dropoff = rides.getLocation(cursor, dropoff)

        # prompt user to enter how much they're willing to pay
        amount = input('How much are you willing to pay per seat? ')
        while amount.isdigit() == False:
            amount = input("Invalid input. Enter a numerical amount: ")
        amount = int(amount) # make sure it is an integer!

        # get rid from function
        rid = getReqID(cursor, conn, email)

        # insert request into table!!!!! then commit
        cursor.execute('''INSERT INTO requests
                VALUES (?, ?, ?, ?, ?, ?);''', (rid, email, date, pickup, dropoff, amount))
        conn.commit()

        print('Ride Request Posted!')
        break

def searchDeleteRequest(cursor, conn, email):
    # display options for what user is able to do with ride requests and other stuff
    clear()
    print('''Ride Request Management''')
    print('-----------------------------------------------------------')
    print("1 - View/Delete Your Ride Requests")
    print("2 - Search Ride Requests")
    print("3 - Go Back")

    while True:
        # wait for input / take in input
        selection = input('Please enter 1, 2, or 3: ')
        if selection == '1':
            manageYourRequests(cursor, conn, email)
            break
        elif selection == '2':
            searchRequest(cursor, conn, email)
            break
        elif selection == '3':
            break
        else:
            print('Invalid choice try again!')
            continue

def manageYourRequests(cursor, conn, email):
    # view and manage YOUR requests i.e. whoever is logged in can look
    # at their own requests and do a bunch of things
    clear()
    while True:
    # query all the ride requests and then print them to the screen
    # ASSUMING THAT THE 5 PER PAGE DISPLAY DOES NOT APPLY DUE TO VAGUE WORDING!!!!
        cursor.execute(''' SELECT * FROM requests WHERE email = ?''', (email,))
        requests = cursor.fetchall()

        if len(requests) == 0: # see if no ride requests
            print('You have no ride requests!')
            break
        else: # otherwise print all of them requests
            print("Your Ride Requests:")
            print("ID | Date | Pickup | Dropoff | Amount")
            for request in requests:
                print(str(request[0]) + " | " + str(request[2]) + " | " + str(request[3]) + " | " + str(request[4]) + " | " + str(request[5]))
            print("\n")

            # if wanna delete, prompt to enter an ID number
            print("If you wish to delete a ride request, enter the ID of the ride request you wish to delete.")
            delOption = input("Otherwise, enter anything else: ")
            delCheck = re.match("^[\d]+$", delOption)

            # if nothing matches, then break out
            if delCheck is None:
                break

            else:
                # if there is something, fetch all the ride numbers associated with the email
                cursor.execute("SELECT rid FROM requests WHERE email = ?;", (email,))
                get = cursor.fetchall()
                ridNums = set() # initialize a set of rides

                for tuple in get:
                    # put rid's into the set
                    if tuple[0] not in ridNums:
                        ridNums.add(tuple[0])

                if int(delOption) in ridNums: # if input is a valid RID then like delete it
                    cursor.execute("DELETE FROM requests WHERE rid = ?", (delOption,))
                    conn.commit()
                    print("Ride Request Deleted!")
                    break
                else: # otherwise try AGAIN
                    print("\nID not found. Try a different ID that you have access to or exit.")
                    continue

def searchRequest(cursor, conn, email):
    # search for a ride request
    clear()
    sentMessage = 0
    exitWanted = 0
    while True:
        filter = input("Enter a pickup location code or city to find ride requests: ").lower()

        # get the ride requests with the inputted pickup location
        cursor.execute(''' SELECT DISTINCT requests.rid, requests.email, requests.rdate, requests.pickup,
                            requests.dropoff, requests.amount
                            FROM locations, requests
                            WHERE lcode = ? AND pickup = lcode;''', (filter,))

        # get the filtered list of riderequests
        filteredRequests = cursor.fetchall()
        numRequests = len(filteredRequests)

        if (numRequests == 0):
            # if cant match a location code, then match a CITY not KEYWORD as specified
            cursor.execute(''' SELECT DISTINCT city FROM locations;''')
            allLocations = cursor.fetchall()
            # create a location set and add the locations found into it
            locationSet = set()
            for location in allLocations:
                locationSet.add(location[0].lower())

            # if no requests with given location, break
            if filter not in locationSet:
                print("There are no ride requests with the given pickup location.")
                break

            else:
            # otherwise, there are requests with the given location so like fetch
            # all the ride request data associated with that city name
                cursor.execute(''' SELECT DISTINCT requests.rid, requests.email, requests.rdate, requests.pickup,
                                    requests.dropoff, requests.amount
                                    FROM locations, requests
                                    WHERE city LIKE ?;''', (filter,))
                filteredRequests = cursor.fetchall()

        # display ALL the requests and like filter with 5 per page
        print("Ride Requests with Pickup Location: " + filter)
        print("ID | Date | Pickup | Dropoff | Amount | Poster")
        ridSet = set()
        counter = 0
        filteredRequestsNum = len(filteredRequests)
        while True:
            if counter < filteredRequestsNum:
                request = filteredRequests[counter]
                ridSet.add(int(request[0]))
                print(str(request[0]) + " | " + str(request[2]) + " | " + str(request[3]) + " | " + str(request[4]) + " | " + str(request[5]) + " | " + str(request[1]))

                counter += 1
            # Mod 5 will say we have reach 5th entry or equal to length means end of list
            if counter % 5 == 0 or counter == filteredRequestsNum:
                if counter == filteredRequestsNum:
                    print('End of the list')
                print("If you wish to message a poster about a ride, enter the ID number of the ride request. ")
                msgNum = input("Enter 'EXIT' to exit the search. Otherwise, enter anything else to see next 5: ").upper()
                # Check which command to do next
                if msgNum.isdigit() == False:
                    if msgNum == 'EXIT':
                        exitWanted = 1
                        break
                    else:
                        continue
                else:
                    # Ask again if the id entered is not in the set
                    while True:
                        msgNum = int(msgNum)
                        if msgNum not in ridSet:
                            msgNum = input("ID not in listing. Try again: ")
                            continue
                        else:
                            break
                # Get the email of the person who posted the request
                cursor.execute(''' SELECT email FROM requests WHERE rid = ?;''', (msgNum,))
                poster = cursor.fetchone()[0]
                messagePoster(cursor, conn, email, msgNum, poster)
                sentMessage = 1
                break
        # Exit if exit chosen or a message was sent
        if sentMessage == 1 or exitWanted == 1:
            break

def messagePoster(cursor, conn, email, msgNum, poster):
    # have member/user message whoever posted a ride request
    # take inputs as appropriately
    clear()
    while True:
        # take message as input
        message = input("Enter the message you wish to send to " + str(poster) + " about ride #" + str(msgNum)+ ": ")

        # get the rno of the ride request from the poster and the rid inputted by the user
        cursor.execute('''SELECT rides.rno FROM rides, requests
                        WHERE requests.email = ?
                            AND requests.rid = ? AND rides.rdate = requests.rdate
                            AND rides.src = requests.pickup AND rides.dst = requests.dropoff;''', (poster, msgNum))
        rnoFetched = cursor.fetchone()

        # if rno is found, then SEND THE MESSAGE!!!!!!
        if rnoFetched is not None:
            rno = rnoFetched[0]
            cursor.execute(''' INSERT INTO inbox VALUES (?,datetime('now'),?,?,?,'n');''', (poster, email, message, rno))
            conn.commit()
            print('Message sent!')
            break
        else:
            # otherwise, if no rno is found, then say there is nothing and like break out i guess
            print('No rides available matching this request.')
            break
