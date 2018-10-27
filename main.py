import getpass
import sqlite3
from os import system, name
from tables import *
from bookings import *
from login import *
from modifyrequests import *
from offer import *
from postrequests import *
from searchrides import *

connection = None
cursor = None

'''
WAITING FOR USER INPUT
 https://www.quora.com/How-do-you-make-a-command-to-wait-for-the-user-to-press-ENTER-in-
Clear command window
 https://www.geeksforgeeks.org/clear-screen-python/
'''

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def main():
    ''' initialize application or something'''
    conn = sqlite3.connect("./movie.db") # creates or opens a db in that path
    # CHANGE ./movie.db TO DATABASE WE WILL USE FOR OUR DATA OR WHATEVER
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;') # set foreign key constraint
    create_tables(cursor, conn)

    email = None

    print('-----------------------------------------------------------')
    print('Welcome to UberLite')
    print('-----------------------------------------------------------')
    print('Login or Register a new user')
    while True:
        print('1 - Login')
        print('2 - Register new user')
        selection = int(input())
        if selection == 1:
            email = getLogin(cursor, conn)
            break
        elif selection == 2:
            email = registerNewUser(cursor, conn)
        else:
            print('Invalid Selection. Try Again')
            continue
    # DO LOGIN PAGE STUFF HERE???
    print('enter a number corresponding to whatever whatever below')
    print('1 - offer a ride')
    print('2 - search for rides')
    print('3 - book members or cancel bookings')
    print('4 - post ride requests')
    print('5 - search and delete ride requests')

    user_input = int(input())

    if (user_input == 1):
        print('call offer ride stuff')

    if (user_input == 2):
        print('search for rides')

    if (user_input == 3):
        print('booking shit')

    if (user_input == 4):
        print('post ride requests')

    if (user_input == 5):
        print('search and delete ride requests')

    if (user_input == 420):
        print('blaze it')


    # COMMIT CHANGES AND THEN CLOSE THE CONNECTION to DATABASE THINGY
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
