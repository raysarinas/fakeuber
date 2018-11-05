# login page stuff
''' Python Regex Phone Number https://stackoverflow.com/questions/15258708/python-trying-to-check-for-a-valid-phone-number
	Python Regex Email https://stackoverflow.com/questions/8022530/python-check-for-valid-email-address
	Python Regex Syntax https://docs.python.org/3/library/re.html
	Hide Password https://pymotw.com/2/getpass/
'''
import re
import getpass
def getLogin(cursor, conn):
	print('Login')

	while True:
		# User inputs their email
		email = input('Enter Email:').lower()
		# Check valid email
		emailCheck = re.match("^[\\_\d\w]+\\@[\\_\d\w]+\\.[\\_\d\w]+$", email)
		# Get password
		password = getpass.getpass(prompt="Enter Password: ")
		# Check valid password
		passwordCheck = re.match("^[\\_\d\w]+$", password)
		# If both valid, find if exists in table
		if passwordCheck and emailCheck:
			cursor.execute('''SELECT * FROM members WHERE email LIKE ? AND pwd=?;''', (email,password))
			rows = cursor.fetchall()
			# No matching email and password
			if not rows:
				print('Login failed: Email/Password are incorrect. Try Again')
				continue
			# Login Successful
			else:
				print('Login Successful!')
				break
		# Entered email/password were invalid
		else:
			print('Invalid email/password. Try Again')

	# Get all unread messages
	cursor.execute('''SELECT DISTINCT content, msgTimestamp FROM inbox
								WHERE email LIKE ? AND seen='n';''',(email,))
	rows = cursor.fetchall()
	# Check if messages are there
	if rows:
		print('Your Unread Messages')
		print('-----------------------------------------------------------')
		# For each message print and change to seen
		for x in rows:
			content = 0
			timestamp = 1
			print(x[content])
			cursor.execute('''UPDATE inbox SET seen='y'
									WHERE email LIKE ? AND msgTimestamp=?;''',
									(email, x[timestamp]))
		# Commit changes
		conn.commit()
	# If empty, no new messages to display
	else:
		print('You have no new messages')
	# User is now logged in
	return email

def registerNewUser(cursor, conn):
	print('Register a new user')
	# User enters their email
	while True:
		email = input('Enter Email: ').lower()
		emailCheck = re.match("^[\\_\d\w]+\\@[\\_\d\w]+\\.[\\_\d\w]+$", email)
		# Check valid email
		if emailCheck is None:
			print('Not an email. Try Again')
			continue
		# Check if email is unique
		cursor.execute('SELECT * FROM members WHERE email LIKE ?;', (email,))
		rows = cursor.fetchall()
		# not rows means email exists therefore is not unique
		if not rows:
			break
		else:
			print('Email already exists. Use a different email')
			continue

	# User inputs their name
	while True:
		name = input('Enter your Name(Can contain spaces, "-" and "."): ')
		nameCheck = re.match("^[\-\.\w\ ]+$", name)
		# Check if no name was entered
		if not name:
			print('No name entered. Please enter a name')
			continue
		elif nameCheck is None:
			print('Invalid name entered.')
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
			break
	# User inputs their password
	while True:
		password = getpass.getpass(prompt="Enter Your Password: ")
		# Check if no password was entered or invalid
		passwordCheck = re.match("^[\\_\d\w]+$", password)
		if not password or passwordCheck is None:
			print('Invalid password. Please enter a password')
			continue
		else:
			break
	cursor.execute('''INSERT INTO members VALUES (?, ?, ?, ?);''', (email, name, phone, password))
	conn.commit()
	print('New Account created!')
	return email
