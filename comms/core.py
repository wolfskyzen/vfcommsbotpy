#!/usr/bin/python
from telegram.ext import CommandHandler
from telegram.ext import Updater

from comms import handlers

class Core:
    updater = None        
    
    def setup(self, token):
        print("Setting up bot")
        self.updater = Updater(token)
        if self.updater == None:
            print("Failed to setup Telegram Updater")
            return
        handlers.setup(self.updater.dispatcher)
        self.verify()

    def verify(self):
        if self.updater == None:
            print("Telegram Updater not setup!")
        else:
            print("Verifying bot")
            print(self.updater.bot.getMe())

    def run(self):
        if self.updater != None:
            print("Running...")
            self.updater.start_polling()

    def stop(self):
        if self.updater != None:
            print("Stopping...")
            self.updater.stop()
            self.updater = None
        print("Done!")
