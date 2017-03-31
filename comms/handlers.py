#!/usr/bin/python
from telegram.ext import Dispatcher

"""
    Add any and all command handlers here
"""
def setup(dispatcher):
    from comms import whois
    whois.setup_handler(dispatcher)
