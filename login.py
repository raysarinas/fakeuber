# login page stuff
# Python Regex Phone Number https://stackoverflow.com/questions/15258708/python-trying-to-check-for-a-valid-phone-number
# {ython Regex Syntax https://docs.python.org/3/library/re.html}
import re
import getpass
def getLogin(cursor):
	while(true):
		email = ""
		password = ""
		print('-----------------------------------------------------------')
		print('Welcome to Knockoff Uber')
		print('-----------------------------------------------------------')
		print('Login')
		email = input('Enter Email:')
		password = getpass.getpass(prompt="Enter Password: ")
		cursor.execute('SELECT * FROM members WHERE email=? AND pwd=?;', (email,password))
		rows = cursor.fetchall()
		if not rows:
			print('Login failed: Invalid email/password. Try Again')
			continue
		else:
			print('Login Successful!')
			break

def registerNewUser(cursor):
	while(true):
		email = ""
		password = ""
		name = ""
		phone = ""
		name = input('Enter your Name: ')
		phone = input('Enter your Phone Number (###-###-#### format): ')
		phoneCheck= re.match("^[\d]{3}-[\d]{3}-[\d]{4}$", phone)
		if phoneCheck is None:
			continue
		
