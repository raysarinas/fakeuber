import getpass
import sqlite3
from os import system, name, path
from sys import exit
from clear import clear
import re
from login import *
import module

connection = None
cursor = None

def test_getLogin():
    mockdb = './test.db'
    conn = sqlite3.connect(mockdb)
    cursor = conn.cursor()

    # override built-in input() function i guess
    module.input = lambda: "test@test.ca"

# https://stackoverflow.com/questions/35851323/how-to-test-a-function-with-input-call



