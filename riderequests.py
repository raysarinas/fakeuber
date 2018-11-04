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
    clear() # do i need to import something so this works or what
    print('Post a Ride Request by entering the following information: ')

    conn.commit()

    counter = 0
    while True:
        date = input('Ride Date (YYYY-MM-DD)?')
        dateCheck = re.match("^[\d]{4}\\-[\d]{2}\\-[\d]{2}$", date)
        if dateCheck is None:
            print('Invalid Date. Try Again')
            continue
        # CALL rides.getLocation AS PICKUP AND DROPOFF
        pickup = rides.getLoc(cursor, conn, email)
        dropoff = rides.getLoc(cursor, conn, email)
        amount = input('How much are you willing to pay per seat? ')
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

# def displayUserRequests(cursor, conn, email):
#     clear()
#     requests = cursor.fetchall()
#     if len(requests) == 0:
#         print('You have no ride requests!')
#     else:
#         print("ID | Date | Pickup | Dropoff | Amount")
#         for request in requests:
#             print(str(request[0]) + " | " + str(request[2]) + " | " + str(request[3]) + " | " + str(request[4]) + " | " + str(request[5]))
#         print("\n")

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
                cursor.execute("SELECT rid FROM requests")
                get = cursor.fetchall()
                ridNums = set()

                for tuple in get:
                    if tuple[0] not in ridNums:
                        ridNums.add(tuple[0])

                if delete in ridNums: # if input is a valid RID then like delete it
                    cursor.execute("DELETE FROM requests WHERE rid = ?", (delete,))
                    conn.commit()
                    print("Ride Request Deleted!")
                    break
                else:
                    print("ID not found. Try a different ID or exit.")
                    continue

# def deleteRequest(cursor, conn, email):
#     clear()
#     #getAllRequests(cursor, conn, email)
#     while True:
#
#         print("Otherwise, enter an")
#         delete = int(input("Enter the ID of the ride request you wish to delete: "))
#
#         cursor.execute("SELECT rid FROM requests")
#         get = cursor.fetchall()
#         ridNums = set()
#         for tuple in get:
#             if tuple[0] not in ridNums:
#                 ridNums.add(tuple[0])
#
#         if delete in ridNums: # if input is a valid RID then like delete it
#             cursor.execute("DELETE FROM requests WHERE rid = ?", (delete,))
#             conn.commit()
#             print("Ride Request Deleted!")
#             break
#         else:
#             print("ID not found. Try a different ID or exit.")
#             continue


def searchRequest(cursor, conn, email):
    clear()
    while True:
        clear()
        # SHOULD HAVE OPTION TO SELECT LOCATION CODE OR CITY AS INPUT?
        # OR SHOULD JUST AUTOMATICALLY TRY TO CHECK?
        filter = input("Enter a pickup location code or city to find ride requests: ")

        # get the ride requests with the inputted pickup location
        # FIX THIS QUERY WHEN ACTUALLY NOT DYING
        cursor.execute(''' SELECT DISTINCT requests.rid, requests.email, requests.rdate, requests.pickup,
                            requests.dropoff, requests.amount
                            FROM locations, requests
                            WHERE lcode = ? AND pickup = lcode;''', (filter,))
        filteredRequests = cursor.fetchall()
        numRequests = len(filteredRequests)

        # NEED TO FILTER OUT ONLY 5 PER PAGE????

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

            # EMAIL CHECKER NOT WORKING??A?FGSFN?GDGSFDGSFDHGSfdfgfdgn
            emailCheck = re.match("^[_\d\w]+\\@[_\d\w]+\\.[_\d\w]+$", emailMember)

            if emailMember is None:
                print('Invalid email. Try again?')
                continue
            else:
                #break
                messagePoster(cursor, conn, email, emailMember)
                # RIGHT HERE SHOULD BE ABLE TO MESSAGE MEMBER



        # get number of filteredRequests
        # TODO: FINISH THIS QUERY PROBABLY??? NOT SURE IF ITS ACTUALLY DONE
        # PART OF THIS SHOULD BE IN THE ELSE WHILE TRUE COUNTER LOOP!!!!
        counter = 0
        cursor.execute(''' SELECT DISTINCT COUNT(requests.*) as num
                                    FROM rides, requests, locations
                                    WHERE requests.email = ? AND requests.pickup = ?
                                    LIMIT ?, 5;''', (email, filter, counter))
        reqs = cursor.fetchone()
        numReqs = reqs["num"]


        if rides == []:
            print("No rides matched. Try again?")
            continue

        else:
            while True:
                if counter < numReqs:
                    # FIX THIS QUERY LATER I GUESS ????
                    cursor.execute(''' SELECT DISTINCT COUNT(requests.*) as num
                            FROM rides, requests, locations
                            WHERE requests.email = ? AND requests.pickup = ?
                            LIMIT ?, 5;''', (email, filter, counter))

                else:
                    print("END of List")

                # REWRITE THIS SINCE THIS IS FROM JACOB'S BOOKINGS CRAP
                # COULD PUT BOTH STUFF/THINGS INTO SEPARATE FUNCTIONS POTENTIALLY
                selectMore = input('Enter "NEXT" to see more rides, "BOOK" to book a member on your ride').upper()
                if selectMore == "NEXT":
                    counter += 5
                    continue
                elif selectMore == "BOOK":
                    getBookingInfo(loginEmail, userOffers, cursor, conn)
                elif selectMore == "EXIT":
                    break
                else:
                    print('Invalid command entered. Try again')

def messagePoster(cursor, conn, email, poster):
    clear()
    # EMAILING/MESSAGING BETWEEN MEMBERS???
    # put crap into a table and then like do stuff i guess
    # just INSERT message into the email table
    # and then like have an option to like display the email or whatever i guess

    while True:
        message = input("Enter the message you wish to send to " + poster + ": ")
        timeStamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        rno = 0 # NEED TO CHANGE THIS SO CAN GET FROM RIDES RNO SHIT
        cursor.execute(''' INSERT INTO inbox VALUES (?,?,?,?,?,'n');''', (poster, timeStamp, email, message, rno))
        conn.commit()
        print('Message sent!')
        # values = (str(ride[7]), t, loginEmail, message, str(ride[0]), "n" )
        # query = "INSERT INTO inbox VALUES(?,?,?,?,?,?);"
        # runSQL(c, conn, query, values)
        #print("Message sent!\n")
        break
