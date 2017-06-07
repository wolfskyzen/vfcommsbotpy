#!/usr/bin/python
from comms.core import Core

def stop():
    core.stop()

def get_token():
    tokenfile = open("var/TOKEN")
    token = tokenfile.readline()
    return token

if __name__ == "__main__":
    tokenstr = get_token()
    if tokenstr:
        try:
            core = Core()
            core.setup(tokenstr)
            core.run()
        except:
            print(sys.exc_info())
    else:
        exit(1)
