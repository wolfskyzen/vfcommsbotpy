#!/usr/bin/python
from telegram.ext import Dispatcher

"""
    Add any and all command handlers here
"""
def setup(dispatcher):
    from comms import about
    about.setup_handler(dispatcher)
    from comms import broadcaster
    broadcaster.setup_handler(dispatcher)
    from comms import users
    users.setup_handler(dispatcher)
    from comms import whois
    whois.setup_handler(dispatcher)
