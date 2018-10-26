import getpass
import sqlite3
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
 https://www.quora.com/How-do-you-make-a-command-to-wait-for-the-user-to-press-ENTER-in-Python
'''

def main():
    ''' initialize application or something'''
    conn = sqlite3.connect("./movie.db") # creates or opens a db in that path
    # CHANGE ./movie.db TO DATABASE WE WILL USE FOR OUR DATA OR WHATEVER

	cursor = conn.cursor()
	cursor.execute('PRAGMA foreign_keys=ON;') # set foreign key constraint
    create_tables(cursor)

    print('-----------------------------------------------------------')
    print('Welcome to Knockoff Uber')
    print('-----------------------------------------------------------')

    # DO LOGIN PAGE STUFF HERE???
    getLogin(cursor)
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
