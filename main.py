#!/usr/bin/python
from comms import core

def stop():
    core.stop()

def get_token():
    tokenfile = open("var/TOKEN")
    token = tokenfile.readline()
    return token

if __name__ == "__main__":
    token = get_token()
    if token:
        core.setup(token)
        core.run()
    else:
        exit(1)
