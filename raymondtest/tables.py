import sqlite3

def make(cursor, conn):
    pass
    '''
    may or may not have to hard code in the SQL statements that are given
    to build the table???? or could just parse the prj-tables.sql file mayhaps
    '''

def create_tables(cursor, conn):
    #TODO: PARSE THE prj-tables.sql FILE INTO HERE?
    # fh = open("prj-tables.sql", "r")
    # print(fh.readlines())
    cursor.executescript('''

    drop table if exists requests;
    drop table if exists enroute;
    drop table if exists bookings;
    drop table if exists rides;
    drop table if exists locations;
    drop table if exists cars;
    drop table if exists members;
    drop table if exists inbox;

    PRAGMA foreign_keys = ON;

    create table members (
      email		char(15),
      name		char(20),
      phone		char(12),
      pwd		char(6),
      primary key (email)
    );
    create table cars (
      cno		int,
      make		char(12),
      model		char(12),
      year		int,
      seats		int,
      owner		char(15),
      primary key (cno),
      foreign key (owner) references members
    );
    create table locations (
      lcode		char(5),
      city		char(16),
      prov		char(16),
      address	char(16),
      primary key (lcode)
    );
    create table rides (
      rno		int,
      price		int,
      rdate		date,
      seats		int,
      lugDesc	char(10),
      src		char(5),
      dst		char(5),
      driver	char(15),
      cno		int,
      primary key (rno),
      foreign key (src) references locations,
      foreign key (dst) references locations,
      foreign key (driver) references members,
      foreign key (cno) references cars
    );
    create table bookings (
      bno		int,
      email		char(15),
      rno		int,
      cost		int,
      seats		int,
      pickup	char(5),
      dropoff	char(5),
      primary key (bno),
      foreign key (email) references members,
      foreign key (rno) references rides,
      foreign key (pickup) references locations,
      foreign key (dropoff) references locations
    );
    create table enroute (
      rno		int,
      lcode		char(5),
      primary key (rno,lcode),
      foreign key (rno) references rides,
      foreign key (lcode) references locations
    );
    create table requests (
      rid		int,
      email		char(15),
      rdate		date,
      pickup	char(5),
      dropoff	char(5),
      amount	int,
      primary key (rid),
      foreign key (email) references members,
      foreign key (pickup) references locations,
      foreign key (dropoff) references locations
    );
    create table inbox (
      email		char(15),
      msgTimestamp	date,
      sender	char(15),
      content	text,
      rno		int,
      seen		char(1),
      primary key (email, msgTimestamp),
      foreign key (email) references members,
      foreign key (sender) references members,
      foreign key (rno) references rides
    );

    ''')

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

    print('hello')
    conn = sqlite3.connect("./test.db") # creates or opens a db in that path
    cursor = conn.cursor()
    create_tables_test(cursor, conn)

    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movie')
    one_row = cursor.fetchone()
    print('hello')
    print(one_row)
