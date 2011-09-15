import os

def CLS(numlines=100):
    '''Clear the screen in an os friendly way'''
    if os.name == "posix":
        os.system('clear')
    elif os.name in ("nt", "dos", "ce"):
        os.system('CLS')
    else:
        print '\n' * numlines