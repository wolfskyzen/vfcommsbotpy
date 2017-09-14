#!/usr/bin/python
from telegram import Chat
from telegram.ext import CommandHandler
from telegram.ext import Filters
import os
import subprocess
import sys

revision = None

def handle_about(bot, update):
    message = "VancouFur Staff Communications Bot" + os.linesep
    global revision
    if revision is not None:
        message = message + "Version 2.1 ({0})".format(revision) + os.linesep
    else:
        message = message + "Version 2.1" + os.linesep
    message = message + "Created by Zen using the Python Telegram Bot API." + os.linesep
    message = message + "Bugfixes by Maxwolf as seen on TV!" + os.linesep
    message = message + "https://github.com/wolfskyzen/vfcommsbotpy"
    bot.sendMessage(chat_id=update.message.chat_id, text=message, reply_to_message_id=update.message.message_id)
    
def setup():
    try:
        global revision
        revisionfile = open("var/REVISION")
        revision = revisionfile.readline()
        revision = revision.strip()        
    except:
        print("Unable to get current local git revision")
        print(sys.exc_info())
    
def setup_handler(dispatcher):
    setup()
    handler = CommandHandler('about', handle_about, Filters.command)
    dispatcher.add_handler(handler);
