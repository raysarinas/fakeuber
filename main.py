import getpass
import sqlite3
from os import system, name
import os.path
from sys import exit
from rides import *
from bookings import *
from riderequests import *
from login import *
from clear import clear

connection = None
cursor = None

def exitProgram(conn):
    print("ok bye program exited")
    conn.commit()
    conn.close()
    exit()

def main():
    # initialize everything i guess
    clear()
    db = input('Enter a database to use (with .db extension): ') #"./uberDB.db"
    #db = './uberDB.db'
    check = os.path.isfile(db)
    conn = sqlite3.connect(db) # creates or opens a db in that path
    cursor = conn.cursor()

    cursor.execute('PRAGMA foreign_keys=ON;') # set foreign key constraint

    clear()
    print('-----------------------------------------------------------')
    print('Welcome to UberLite')
    print('-----------------------------------------------------------')
    print('Login or Register a new user')

    email = None

    while True:
        # wait for user to select/enter to do something
        print('Enter 1 or 2 to log in or register as a new user. ')
        print('Otherwise, enter anything else to exit program. ')
        print('1 - Login')
        print('2 - Register New User')
        selection = input()
        clear()
        if selection == '1':
            email = getLogin(cursor, conn)
            break
        elif selection == '2':
            email = registerNewUser(cursor, conn)
            break
        else:
            exitProgram(conn)

    # display functionalities
    systemFunctionalities(cursor, conn, email)
    exitProgram(conn) # close the database? exit program

def systemFunctionalities(cursor, conn, email):
    # display and allow user to pick different things to do in the program
    print('-----------------------------------------------------------')
    print('Watcha wanna do? Enter a number below to continue or anything else to exit')
    print('1 - offer a ride')
    print('2 - search for rides')
    print('3 - book members or cancel bookings')
    print('4 - post ride requests')
    print('5 - search and delete ride requests')
    print('6 - log out')

    user_input = input()

    if (user_input == '1'):
        clear()
        offerRide(cursor, conn, email)

    if (user_input == '2'):
        clear()
        searchRides(cursor, conn, email)

    if (user_input == '3'):
        clear()
        getBookings(email, cursor, conn)

    if (user_input == '4'):
        clear()
        postRequest(cursor, conn, email)

    if (user_input == '5'):
        clear()
        searchDeleteRequest(cursor, conn, email)

    if (user_input == '6'):
        logout()
        #exitProgram(conn)

    if (user_input == "420"):
        print('blaze it')

    while True:
        # ask if user wants to continue if input is wrong or incorrect
        # also break out into this when user finished operating/using a certain functionality
        cont = str(input('Do you want to continue? \nEnter 1 to Continue, otherwise exit/logout: '))

        if cont is '1':
            # if want to continue, clear screen and display functionality options again
            clear()
            systemFunctionalities(cursor, conn, email)
        else:
            # otherwise, log out
            logout()

def logout():
    # log out just jumps out and restarts program
    main()

def exitProgram(conn):
    # exit the program and then close the database
    print("ok bye program exited")
    conn.commit()
    conn.close()
    exit()

if __name__ == "__main__":
    main()
    exit()
