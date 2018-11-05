# 4 - POST RIDE REQUESTS
# 5 - SEARCH AND DELETE RIDE requests

import re, rides, datetime, time
from os import system, name

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

''' could potentially combine the ride request functions into
    one function and like just have different options for functionalities
    like in Kathleen's code? with home function in requests.py '''


# COMBINE getRideNum and getReqID into one function that takes
# the table as another parameter so dont have too much redundant code?
def getReqID(cursor, conn, email):
    cursor.execute(''' SELECT MAX(requests.rid) FROM requests;''')
    last = cursor.fetchall()
    if last == None:
        return 1
    rid = int(last[0][0])+ 1
    return rid



def postRequest(cursor, conn, email):
    '''
    The member should be able to post a ride request by providing a date,
    a pick up location code, a drop off location code, and the amount willing
    to pay per seat. The request rid is set by your system to a unique number
    and the email is set to the email address of the member.
    '''
    clear()
    print('Post a Ride Request by entering the following information: ')

    while True:
        date = input('Ride Date (YYYY-MM-DD)? ')
        dateCheck = re.match("^[\d]{4}\\-[\d]{2}\\-[\d]{2}$", date)
        if dateCheck is None:
            print('Invalid Date. Try Again')
            continue
        else: # CONVERT TO DATE TYPE
            year, month, day = map(int, date.split('-'))
            date = datetime.date(year, month, day)
        #print(date)
        #print(type(date))
        pickup = input("Enter a pickup location code or keyword: ")
        pickup = rides.getLocation(cursor, pickup) #rides.getLoc(cursor, conn, email).replace("%", "")
        #print(pickup)
        dropoff = input("Enter a dropoff location code or keyword: ")
        dropoff = rides.getLocation(cursor, dropoff) #rides.getLoc(cursor, conn, email).replace("%", "")
        #print(dropoff)

        amount = input('How much are you willing to pay per seat? ')

        while amount.isdigit() == False:
            amount = input("Invalid input. Enter a numerical amount: ")
        amount = int(amount)

        rid = getReqID(cursor, conn, email)
        cursor.execute('''INSERT INTO requests
                VALUES (?, ?, ?, ?, ?, ?);''', (rid, email, date, pickup, dropoff, amount))
        conn.commit()

        print('Ride Request Posted!')

        break

def searchDeleteRequest(cursor, conn, email):
    '''
    The member should be able to see all his/her ride requests and be able
    to delete any of them. Also the member should be able to provide a
    location code or a city and see a listing of all requests with a pickup
    location matching the location code or the city entered. If there are more
    than 5 matches, at most 5 matches will be shown at a time. The member
    should be able to select a request and message the posting member, for
    example asking the member to check out a ride.
    '''
    clear()
    print('''Ride Request Management''')
    print('-----------------------------------------------------------')
    print("1 - Manage Your Ride Requests")
    print("2 - Search Ride Requests")
    print("3 - Message Posting Member")
    print("4 - Go Back")

    while True:
        selection = input('Please enter 1, 2, 3, or 4: ')
        if selection == '1':
            manageYourRequests(cursor, conn, email)
            break
        elif selection == '2':
            searchRequest(cursor, conn, email)
            break
        elif selection == '3':
            print('default will message to don@mayor.yeg because cant test out otherwise?')
            messagePoster(cursor, conn, email, 'don@mayor.yeg')
            break
        elif selection == '4':
            break
        else:
            print('Invalid choice dum dum')
            continue

def manageYourRequests(cursor, conn, email):
    clear()
    while True:
    # query all the ride requests and then print them to the screen
        cursor.execute(''' SELECT * FROM requests WHERE email = ?''', (email,))
        requests = cursor.fetchall()
        if len(requests) == 0:
            print('You have no ride requests!')
            break
        else:
            print("Your Ride Requests:")
            print("ID | Date | Pickup | Dropoff | Amount")
            for request in requests:
                print(str(request[0]) + " | " + str(request[2]) + " | " + str(request[3]) + " | " + str(request[4]) + " | " + str(request[5]))
            print("\n")
            print("If you wish to delete a ride request, enter the ID of the ride request you wish to delete.")
            delOption = input("Otherwise, enter anything else: ")
            delCheck = re.match("^[\d]+$", delOption)

            if delCheck is None:
                break

            else:
                cursor.execute("SELECT rid FROM requests WHERE email = ?;", (email,))
                get = cursor.fetchall()
                ridNums = set()

                for tuple in get:
                    if tuple[0] not in ridNums:
                        ridNums.add(tuple[0])

                if int(delOption) in ridNums: # if input is a valid RID then like delete it
                    cursor.execute("DELETE FROM requests WHERE rid = ?", (delOption,))
                    conn.commit()
                    print("Ride Request Deleted!")
                    break
                else:
                    print("\nID not found. Try a different ID that you have access to or exit.")
                    continue

def searchRequest(cursor, conn, email):
    clear()
    while True:
        # SHOULD HAVE OPTION TO SELECT LOCATION CODE OR CITY AS INPUT?
        # OR SHOULD JUST AUTOMATICALLY TRY TO CHECK?
        filter = input("Enter a pickup location code or city to find ride requests: ").lower()

        # get the ride requests with the inputted pickup location
        # FIX THIS QUERY WHEN ACTUALLY NOT DYING
        cursor.execute(''' SELECT DISTINCT requests.rid, requests.email, requests.rdate, requests.pickup,
                            requests.dropoff, requests.amount
                            FROM locations, requests
                            WHERE lcode = ? AND pickup = lcode;''', (filter,))
        filteredRequests = cursor.fetchall()
        numRequests = len(filteredRequests)

        if (numRequests == 0):
            cursor.execute(''' SELECT DISTINCT city FROM locations;''')
            allLocations = cursor.fetchall()
            locationSet = set()
            for location in allLocations:
                locationSet.add(location[0].lower())

            if filter not in locationSet:
                print("There are no ride requests with the given pickup location.")
                break

            else:
                cursor.execute(''' SELECT DISTINCT requests.rid, requests.email, requests.rdate, requests.pickup,
                                    requests.dropoff, requests.amount
                                    FROM locations, requests
                                    WHERE city LIKE ?;''', (filter,))
                filteredRequests = cursor.fetchall()

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
            # if filteredRequestsNum > counter:
                counter += 1

            if counter % 5 == 0 or counter == filteredRequestsNum:
                if counter == filteredRequestsNum:
                    print('End of the list')
                print("If you wish to message a poster about a ride, enter the ID number of the ride request. ")
                msgNum = input("Enter 'EXIT' to exit the search. Otherwise, enter anything else to see next 5: ").upper()
                print("input - " + msgNum)
                #emailCheck = re.match("^[_\d\w]+\\@[_\d\w]+\\.[_\d\w]+$", emailMember)

                # while msgNum.isdigit() == False:
                    # msgNum = input("Invalid input. Enter a number: ")
                if msgNum.isdigit() == False:
                    if msgNum == 'EXIT':
                        break
                    else:
                        continue
                else:
                    while True:
                        msgNum = int(msgNum)
                        if msgNum not in ridSet:
                            msgNum = input("ID not in listing. Try again: ")
                            continue
                        else:
                            break

                cursor.execute(''' SELECT email FROM requests WHERE rid = ?;''', (msgNum,))
                poster = cursor.fetchone()[0]
                messagePoster(cursor, conn, email, msgNum, poster)
                break

            # if emailCheck is None:
            #     print('Invalid email. Try again?')
            #     continue
            # else:
            #     #break
            #     messagePoster(cursor, conn, email, emailMember)
            #     # RIGHT HERE SHOULD BE ABLE TO MESSAGE MEMBER

def messagePoster(cursor, conn, email, msgNum, poster):
    clear()
    while True:
        message = input("Enter the message you wish to send to " + str(poster) + " about ride #" + str(msgNum)+ ": ")
        timeStamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('''SELECT rides.rno FROM rides, requests
                        WHERE rides.driver = ? AND rides.driver = requests.email
                            AND requests.rid = ? AND rides.rdate = requests.rdate
                            AND rides.src = requests.pickup AND rides.dst = requests.dropoff;''', (poster, msgNum))
        rnoFetched = cursor.fetchone()

        if rnoFetched == None:
            print('No rides available matching this request. Enter something ')
        print(rnoFetched)
        print("--------")
        break
        rno = 0 # NEED TO CHANGE THIS SO CAN GET FROM RIDES RNO SHIT
        cursor.execute(''' INSERT INTO inbox VALUES (?,?,?,?,?,'n');''', (msgNum, timeStamp, email, message, rno))
        conn.commit()
        print('Message sent!')
        break
