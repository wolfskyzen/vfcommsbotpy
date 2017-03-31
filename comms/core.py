#!/usr/bin/python
from telegram.ext import CommandHandler
from telegram.ext import Updater

from comms import handlers

global updater

def setup(token):
    global updater
    print("Setting up bot")
    updater = Updater(token)
    handlers.setup(updater.dispatcher)
    verify()

def verify():
    global updater
    print("Verifying bot")
    print(updater.bot.getMe())

def run():
    global updater
    print("Running...")
    updater.start_polling()

def stop():
    global updater
    print("Stopping...")
    updater.stop()
    print("Done!")
