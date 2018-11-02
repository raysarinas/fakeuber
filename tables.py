import sqlite3

def make(cursor, conn):
    pass
    '''
    may or may not have to hard code in the SQL statements that are given
    to build the table???? or could just parse the prj-tables.sql file mayhaps
    '''

def create_tables_test(cursor, conn):
    #TODO: PARSE THE prj-tables.sql FILE INTO HERE?
    fh = open("prj-tables.sql", "r")
    print(fh.readlines())
    #cursor.executescript("PARSED FILE DATA INTO HERE")

def test():
    conn = sqlite3.connect("./project.db") # creates or opens a db in that path

    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;') # set foreign key constraint
    # if dont have turned on, can do select statements that violet foreign key so like its not enforced
    # but will do bad things maybe????? like write queries that write things out of constraints?

    create_tables_test(cursor, conn)


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
    for line in fd:
        print(line)
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        pass
        try:
            c.execute(command)
        except (OperationalError, msg):
            print("Command skipped: ", msg)

if __name__ == "__tables__":
    executeScriptsFromFile('prj-tables.sql')
