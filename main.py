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
        core = Core()
        core.setup(tokenstr)
        core.run()
    else:
        exit(1)
