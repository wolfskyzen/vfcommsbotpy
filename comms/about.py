#!/usr/bin/python
from telegram import Chat
from telegram.ext import CommandHandler
from telegram.ext import Filters
import os
import subprocess
import sys

git_version = None

def handle_about(bot, update):
    message = "VancouFur Staff Communications Bot" + os.linesep
    global git_version
    if git_version is not None:
        message = message + "Version 2.0 ({0})".format(git_version) + os.linesep
    else:
        message = message + "Version 2.0" + os.linesep
    message = message + "Created by Zen using the Python Telegram Bot API." + os.linesep
    message = message + "https://github.com/wolfskyzen/vfcommsbotpy"
    bot.sendMessage(chat_id=update.message.chat_id, text=message, reply_to_message_id=update.message.message_id)
    
def setup():
    try:
        global git_version
        git_version = subprocess.check_output("git log --pretty=format:""%h"" -1")
        git_version = git_version.decode("utf-8")
    except:
        print("Unable to get current local git revision")
        print(sys.exc_info())
    
def setup_handler(dispatcher):
    setup()
    handler = CommandHandler('about', handle_about, Filters.command)
    dispatcher.add_handler(handler);
