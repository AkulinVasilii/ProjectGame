import os

def ireader(file):
    if not os.path.exists(file):
        inp = open(file, 'x')
        return '0'
    else:
        inp = open(file, 'r+')
        return inp.read()
    
def iwriter(file, string):
    if not os.path.exists(file):
        inp = open(file, 'x')
        inp.write(string)
        inp.close()
    else:
        inp = open(file, 'w+')
        inp.write(string)
        inp.close()
