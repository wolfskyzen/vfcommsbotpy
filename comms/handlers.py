#!/usr/bin/python
from telegram import Bot
from telegram.ext import Dispatcher
from telegram.ext import Updater

"""
    Add any and all command handlers here
"""
def setup(updater):
    from comms import about
    about.setup_handler(updater.dispatcher)
    from comms import broadcaster
    broadcaster.setup_handler(updater.dispatcher)
    from comms import help
    help.setup_handler(updater.dispatcher)
    from comms import meeting
    meeting.setup_handler(updater.dispatcher, updater.bot)
    from comms import users
    users.setup_handler(updater.dispatcher)
    from comms import whois
    whois.setup_handler(updater.dispatcher)
