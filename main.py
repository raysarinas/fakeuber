import getpass
from bookings import *
from login import *
from modifyrequests import *
from offer import *
from postrequests import *
from searchrides import *

'''
WAITING FOR USER INPUT
 https://www.quora.com/How-do-you-make-a-command-to-wait-for-the-user-to-press-ENTER-in-Python
'''

def main():
    ''' initialize application or something'''
    print('hello i guess')

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

main()
