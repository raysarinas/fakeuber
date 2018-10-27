import sqlite3

def create_tables(cursor, conn):

    # DELETE THE TABLE IF ALREADY EXISTS
    cursor.execute('''DROP TABLE movie;''')

    # THIS IS HOW TO MAKE THE TABLES I GUESS
    cursor.execute('''CREATE TABLE movie (
                                            title TEXT,
                                            movie_number INTEGER,
                                            PRIMARY KEY (title)
                                            );''')

    conn.commit() # commit changes made in transaction

    file = open('prj-tables.sql', 'r')
    sqlFile = file.read()
    file.close()

def executeScriptsFromFile(filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            c.execute(command)
        except OperationalError, msg:
            print "Command skipped: ", msg
