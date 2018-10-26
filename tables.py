import sqlite3

def create_tables(cursor):

    # THIS IS HOW TO MAKE THE TABLES I GUESS
    cursor.execute('''CREATE TABLE movie (
                                            title TEXT,
                                            movie_number INTEGER,
                                            PRIMARY KEY (title)
                                            );''')

    conn.commit() # commit changes made in transaction
