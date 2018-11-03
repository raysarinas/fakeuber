# 4 - POST RIDE REQUESTS
# 5 - SEARCH AND DELETE RIDE requests

import re

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

def seadelRequest(cursor, conn, email):
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
    pass

    while True:
        pass
        # copy JuJu's Display/Search STUFF
        #

def message(conn, email):
    pass
    # EMAILING/MESSAGING BETWEEN MEMBERS???
    # put crap into a table and then like do stuff i guess
    # just INSERT message into the email table
    # and then like have an option to like display the email or whatever i guess
