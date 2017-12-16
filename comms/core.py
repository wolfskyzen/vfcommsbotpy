#!/usr/bin/python
from telegram.ext import CommandHandler
from telegram.ext import Updater

from comms import handlers

class Core:
    updater = None
    
    def handle_error(bot, update, error):
        print("Update {0} encountered error %s".format(update, error))
    
    def run(self):
        if self.updater != None:
            print("Running...")
            self.updater.start_polling()
    
    def setup(self, token):
        print("Setting up bot")
        self.updater = Updater(token)
        if self.updater == None:
            print("Failed to setup Telegram Updater")
            return
        self.updater.dispatcher.add_error_handler(Core.handle_error)
        handlers.setup(self.updater)
        self.verify()
    
    def stop(self):
        if self.updater != None:
            print("Stopping...")
            self.updater.stop()
            self.updater = None
        print("Done!")

    def verify(self):
        if self.updater == None:
            print("Telegram Updater not setup!")
        else:
            print("Verifying bot")
            print(self.updater.bot.getMe())
