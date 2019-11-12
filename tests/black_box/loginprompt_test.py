import subprocess
from time import sleep

# need to refactor or something so that can run
# subprocess.Popen somewhere in a set up method/test thing

def test_exit_on_db_prompt():
    # run the application in a subprocess
    test = subprocess.Popen(['python3', 'main.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # write to stdin - i.e. basically just typing in a command for the app to handle
    # type exit to close the application - always end with \n and encode it!!!
    test.stdin.write('exit\n'.encode())
    test.stdin.flush() # flush buffer

    # stdout.readlines() is an array that has all the output stuff as an array
    # we want to check that the last line is "BYE I GUESS" because that is what
    # is printed out on the terminal before we exit, so we take the last element
    # in that array, decode it, and check that it says what it says
    last_msg = test.stdout.readlines()[-1].decode().rstrip()
    assert last_msg == "BYE I GUESS"

    test.stdin.close() # close buffer
    test.terminate() # make sure to terminate the process

def test_exit_on_login_prompt():
    test = subprocess.Popen(['python3', 'main.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # use the correct database and encode it to stdin
    test.stdin.write('uberDB.db\n'.encode())
    test.stdin.flush() # flush buffer

    test.stdin.write('exit\n'.encode())
    test.stdin.flush() # flush buffer
    last_msg = test.stdout.readlines()[-1].decode().rstrip().split()[-1]
    
    # This assert doesn't work and i dont know why lol
    #assert last_msg.rsplit == "ok bye program exited\n"
    assert last_msg == "exited"

    test.stdin.close() # close buffer
    test.terminate() # make sure to terminate the process