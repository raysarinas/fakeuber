import getpass
import sqlite3
from os import system, name
import os.path
from sys import exit
#from tables import *
from rides import *
from bookings import *
from riderequests import *
from login import *

connection = None
cursor = None

'''
WAITING FOR USER INPUT
 https://www.quora.com/How-do-you-make-a-command-to-wait-for-the-user-to-press-ENTER-in-
Clear command window
 https://www.geeksforgeeks.org/clear-screen-python/
Checking if database exists or not
 https://stackoverflow.com/questions/12932607/how-to-check-if-a-sqlite3-database-exists-in-python
'''

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def exitProgram(conn):
    print("ok bye program exited")
    conn.commit()
    conn.close()
    exit()

'''TEST FUNCTION TO TRY AND POPULATE DATABASE'''
def populate(conn, cursor):
    #data = open("prj-tables.sql", "r")
    data = open('prj-data.sql').read()
    cursor.executescript(data)
    conn.commit()
    # for line in data.readlines():
    #     line = line.strip()
        #print(line)
        #cursor.execute(line)
        #conn.commit()

def main():
    ''' initialize application or something'''

    print('-----------------------------------------------------------')
    print('Welcome to UberLite')
    print('-----------------------------------------------------------')
    print('Login or Register a new user')

    #TODO: PERHAPS CHANGE THIS SO THE DATABASE IS NOT HARDCODED IN??????
    db = "./uberDB.db"
    check = os.path.isfile(db)
    conn = sqlite3.connect(db) # creates or opens a db in that path

    # CHANGE ./movie.db TO DATABASE WE WILL USE FOR OUR DATA OR WHATEVER
    cursor = conn.cursor()
    #populate(conn, cursor)

    if not check: #if db not exists, populate
        populate(conn, cursor)

    cursor.execute('PRAGMA foreign_keys=ON;') # set foreign key constraint
    #create_tables(cursor, conn)

    # TESTING
    #cursor.execute(''' INSERT''')

    email = None

    while True:
        print('1 - Login')
        print('2 - Register New User')
        print('3 - Exit Program')
        selection = int(input())
        if selection == 1:
            email = getLogin(cursor, conn)
            break
        elif selection == 2:
            email = registerNewUser(cursor, conn)
            break
        elif selection == 3:
            exitProgram(conn)
        else:
            print('Invalid Selection. Try Again')
            continue
    # DO LOGIN PAGE STUFF HERE???

    systemFunctionalities(cursor, conn, email)
    exitProgram(conn) # close the database? exit program

def systemFunctionalities(cursor, conn, email):
    print('Watcha wanna do? Enter a number below I guess')
    print('1 - offer a ride')
    print('2 - search for rides')
    print('3 - book members or cancel bookings')
    print('4 - post ride requests')
    print('5 - search and delete ride requests')
    print('6 - exit program and fuck off')

    user_input = int(input())

    if (user_input == 1):
        clear()
        print('call offer ride stuff')
        offerRide(cursor, conn, email)

    if (user_input == 2):
        clear()
        print('search for rides')
        searchRides(cursor, conn, email)

    if (user_input == 3):
        clear()
        print('booking shit')
        getBookings(email, cursor, conn)

    if (user_input == 4):
        clear()
        postRequest(cursor, conn, email)

    if (user_input == 5):
        clear()
        searchDeleteRequest(cursor, conn, email)

    if (user_input == 6):
        exitProgram(conn)

    if (user_input == 420):
        print('blaze it')

if __name__ == "__main__":
    main()
    exit()
