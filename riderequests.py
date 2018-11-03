# 4 - POST RIDE REQUESTS
# 5 - SEARCH AND DELETE RIDE requests

import re

''' could potentially combine the ride request functions into
    one function and like just have different options for functionalities
    like in Kathleen's code? with home function in requests.py '''

def postRequest(cursor, conn, email):
    '''
    The member should be able to post a ride request by providing a date,
    a pick up location code, a drop off location code, and the amount willing
    to pay per seat. The request rid is set by your system to a unique number
    and the email is set to the email address of the member.
    '''
    # TAKE date, pickup code, dropoff code and amount willing to pay
    # as input from USER.
    # need to assign that value with a unique request RID
        # could just use an incrementer so every new one is just +1 from
        # previous request posted or just whatever
    # set email to email address of member
    pass
    clear() # do i need to import something so this works or what
    print('Post a Ride Request by entering the following information: ')
    counter = 0
    while True:
        date = input('Ride Date (YYYY-MM-DD)?')
        dateCheck = re.match("^[\d]{4}+\\-[\d]{4}-[\d]{4}$")
        if dateCheck is None:
            print('Invalid Date. Try Again')
            continue
        # CALL rides.getLocation AS PICKUP AND DROPOFF
        pickup = input('Pickup Code? ')
        dropoff = input('Dropoff Code? ')
        amount = input('How much are you willing to pay per seat? ')

        # clear()
        # print("Date | Pickup | Dropoff | Amount willing to Pay")
        # print(str(date) + " | " + str(pickup) + " | " + str(dropoff) + " | " + str(amount))
        # confirm = input("Confirm the entered information by entering 'Y' or 'N':")
        #
        # if confirm.upper() == 'Y':
        # CALL GET RID
        cursor.execute('''INSERT INTO requests
                VALUES (?, ?, ?, ?, ?, ?)''', (rid, email, date, pickup, dropoff, amount))
        conn.commit()

        # elif confirm.upper() == 'N':
        #     continue
        #
        # else:
        #     print("Invalid")
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
    # display / query ride requests RELATED TO member (i.e. EMAIL)
    # match the query thing with member email
    # INPUT: location code or city and then QUERY and list all requests with
        # pickup location matching INPUT
    # SHOW AT MOST 5 MATCHES
    # SCROLL THROUGH NEXT PAGE????
    # BE ABLE TO MESSAGE THE POSTING MEMBER
        # QUERY using INBOX
        # should be able to query or input something into the inbox table
        # test out using separate examples and stuff probably
    clear()
    print('''Ride Request Management
    -----------------------------------------------------------
    1 - View/Search Your Ride Requests
    2 - Delete Ride Requests
    3 - Message Posting Member
    ''')

    while True:
        selection = input('Please enter 1 or 2: ')
        if selection == 1:
            searchRequest(cursor, conn, email)
        elif selection == 2:
            deleteRequest(cursor, conn, email)
        elif selection == 3:
            message(cursor, conn, email)
        else:
            print('Invalid choice dum dum')
            continue

def getAllRequests(cursor, conn, email):
    # query all the ride requests and then print them to the screen
    cursor.execute(''' SELECT * FROM requests WHERE email = ?''', (email,))
    requests = cursor.fetchall()
    print("ID | Date | Pickup | Dropoff | Amount")
    for request in requests:
        print(request[0] + " | " + request[2] + " | " + request[3] + " | " + request[4] + " | " + request[5])
    print("\n")

def searchRequest(cursor, conn, email):
    clear()
    while True:
        print('''Enter how you want to search or view your ride requests:
        1 - View All
        2 - Filter by Pickup Location ''')

        viewMode = int(input())

        if viewMode == 1:
            getAllRequests(cursor, conn, email)

        elif viewMode == 2:
            # SHOULD HAVE OPTION TO SELECT LOCATION CODE OR CITY AS INPUT?
            # OR SHOULD JUST AUTOMATICALLY TRY TO CHECK?
            filter = input("Enter a pickup location code or city to find ride requests: ")

            # get the ride requests with the inputted pickup location
            # FIX THIS QUERY WHEN ACTUALLY NOT DYING
            cursor.execute(''' SELECT DISTINCT lcode FROM locations, requests
                                WHERE city = ? AND requests.email = ?''', (filter, email))
            filteredRequests = cursor.fetchall()

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

def deleteRequest(cursor, conn, email):
    clear()
    getAllRequests(cursor, conn, email)
    while True:
        delete = input("Enter the ID of the ride request you wish to delete: ")

        ridList = 0 # should call rid function to fetch all rid's???
        # maybe like change this to a set of integers so can find easily
        if delete in ridList: # if input is a valid RID then like delete it
            cursor.execute("DELETE FROM requests WHERE rid = ?", (delete))
            conn.commit()
            print("Ride Request Deleted!")
            break
        else:
            print("ID not found. Try a different ID or exit.")
            continue

def message(cursor, conn, email):
    clear()
    # EMAILING/MESSAGING BETWEEN MEMBERS???
    # put crap into a table and then like do stuff i guess
    # just INSERT message into the email table
    # and then like have an option to like display the email or whatever i guess
