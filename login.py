# login page stuff
''' Python Regex Phone Number https://stackoverflow.com/questions/15258708/python-trying-to-check-for-a-valid-phone-number
	Python Regex Email https://stackoverflow.com/questions/8022530/python-check-for-valid-email-address
	Python Regex Syntax https://docs.python.org/3/library/re.html
	Hide Password https://pymotw.com/2/getpass/
'''
import re
import getpass
def getLogin(cursor):
	print('Login')
	while True:
		email = ""
		password = ""
		email = input('Enter Email:')
		password = getpass.getpass(prompt="Enter Password: ")
		cursor.execute('''SELECT * FROM members WHERE email=? AND pwd=?;''', (email,password))
		rows = cursor.fetchall()
		if not rows:
			print('Login failed: Invalid email/password. Try Again')
			continue
		else:
			print('Login Successful!')
			break
	cursor.execute('''SELECT content, msgTimestamp FROM members m, inbox i
								WHERE m.email=i.email AND seen='n';''')
	rows = cursor.fetchall()
	if rows:
		print('Your Unread Messages')
		print('-----------------------------------------------------------')
		for x in rows:
			print(x["content"])
			cursor.execute('''UPDATE inbox SET seen=?
									WHERE content=? AND msgTimestamp=?;''',
									('y', x["content"], x["msgTimestamp"]))

def registerNewUser(cursor):
	print('Register a new user')
	# User enters their email
	while True:
		email = input('Enter Email: ')
		emailCheck = re.match("^[^@]+@[^@]+\.[^@]+$", email)
		# Check valid email
		if emailCheck is None:
			print('Not an email. Try Again')
			continue
		# Check if email is unique
		cursor.execute('SELECT * FROM members WHERE email=?;', (email,))
		rows = cursor.fetchall()
		# is not None means email exists therefore is not unique
		if rows is not None:
			print('Email already exists. Use a different email')
			continue
		else:
			print('Valid email')
			break
	# User inputs their name
	while True:
		name = input('Enter your Name: ')
		# Check if no name was entered
		if not name:
			print('No name entered. Please enter a name')
			continue
		else:
			break
	# User inputs their phone number
	while True:
		phone = input('Enter your Phone Number (###-###-#### format): ')
		# Check if phone number is in correct format
		phoneCheck= re.match("^[\d]{3}-[\d]{3}-[\d]{4}$", phone)
		if phoneCheck is None:
			print('Invalid Phone Number. Try Again')
			continue
		else:
			print('Valid Phone Number')
	# User inputs their password
	while True:
		password = input('Enter your Password: ')
		# Check if no password was entered
		if not password:
			print('No password entered. Please enter a password')
			continue
		else:
			print('Valid password')
			break
