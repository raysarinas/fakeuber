from os import system, name

def clear():
    # CLEAR THE SCREEN
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
