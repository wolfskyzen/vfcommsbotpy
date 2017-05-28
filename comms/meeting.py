#!/usr/bin/python
import json
import datetime
import os
import sys
from comms import broadcaster
from comms import users
from dateutil import parser
from telegram import Chat
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler

class _SetNextMeetingCommand:
    manager = None
    
    DATETIME, LOCATION, CONFIRM = range(3)
    
    def __init__(self, manager):
        self.manager = manager
        
    def handle_cancel(self, bot, update):
        if update.message.chat.type != Chat.PRIVATE:            
            return ConversationHandler.END
        bot.sendMessage(update.message.from_user.id, "Cancelled!")
        return ConversationHandler.END
    
    def handle_confirm(self, bot, update):
        if update.message.chat.type != Chat.PRIVATE:            
            return ConversationHandler.END
        self.manager.save()
        message = "Next meeting has been set by @{0}".format(update.message.from_user.username)
        message += "\n\n"
        message += self.manager.get_next_meeting()
        broadcaster.broadcast(bot, message)
        return ConversationHandler.END
    
    def handle_datetime(self, bot, update):
        if update.message.chat.type != Chat.PRIVATE:            
            return ConversationHandler.END
        state = _SetNextMeetingCommand.DATETIME
        message = "Unable to determine the date and time from your message."
        try:
            self.manager.date = parser.parse(update.message.text)
            state = _SetNextMeetingCommand.LOCATION
            message = "Please message me with the location of the next meeting."
        except:
            print("Could not set meeting datetime")
            print(sys.exc_info())
        bot.sendMessage(update.message.from_user.id, message)
        return state

    def handle_location(self, bot, update):
        if update.message.chat.type != Chat.PRIVATE:            
            return ConversationHandler.END
        self.manager.location = update.message.text
        message = self.manager.get_next_meeting()
        message = message + "\nIs this correct?"
        bot.sendMessage(update.message.from_user.id, message)
        return _SetNextMeetingCommand.CONFIRM
        
    def handle_setnextmeeting(self, bot, update):
        if update.message.chat.type != Chat.PRIVATE:            
            return ConversationHandler.END
        user_id = update.message.from_user.id
        if not users.is_admin(user_id):
            return ConversationHandler.END
        message = "Please message me with the date and time of the next meeting."
        bot.sendMessage(update.message.chat_id, message)        
        return _SetNextMeetingCommand.DATETIME
        
    def setup(self, dispatcher):
        handler = ConversationHandler(
            entry_points=[CommandHandler('setnextmeeting', self.handle_setnextmeeting, Filters.command)],
            
            states={
                _SetNextMeetingCommand.DATETIME: [MessageHandler(Filters.text, self.handle_datetime)],
                
                _SetNextMeetingCommand.LOCATION: [MessageHandler(Filters.text, self.handle_location)],
                
                _SetNextMeetingCommand.CONFIRM: [MessageHandler(Filters.text, self.handle_confirm)],
            },
            
            fallbacks=[CommandHandler('cancel', self.handle_cancel, Filters.command)]
        )
        dispatcher.add_handler(handler)

class MeetingManager:
    FILE_NAME = 'var/MEETING'
    
    cmd_setnextmeeting = None
    
    date = None
    link = ""
    location = ""
    
    def __init__(self):
        self.cmd_setnextmeeting = _SetNextMeetingCommand(self)
    
    def handle_clearmeeting(self, bot, update):
        if update.message.chat.type != Chat.PRIVATE:
            return
        if not users.is_admin(update.message.from_user.id):
            return
        self.date = None
        self.link = ""
        self.location = ""
        self.save()
        message = "Next meeting information has been cleared."
        bot.sendMessage(update.message.chat.id, message)
        
    def handle_nextmeeting(self, bot, update):
        message = self.get_next_meeting()
        if message is None:
            return
        bot.sendMessage(update.message.chat.id, message)        
        
    def get_next_meeting(self):
        if self.date is None or self.location is None:
            return "The next meeting date is not set."
        datestr = self.date.strftime("%A, %B %d, %Y, %I:%M %p")
        return "The next meeting is {0} at {1}.".format(datestr, self.location)
    
    def load(self):
        if os.path.isfile(self.FILE_NAME) == False:
            return
        root = None
        with open(self.FILE_NAME, 'r') as file:
            root = json.load(file)
            file.close()
        if root is not None:
            self.date = parser.parse(root["date"])
            self.link = root["link"]
            self.location = root["location"]
        
    def save(self):
        json_date = None
        if self.date is not None:
            json_date = self.date.isoformat()
        root = { "date": json_date, "link": self.link, "location": self.location }
        with open(self.FILE_NAME, 'w') as file:
            json.dump(root, file, indent=4)
            file.close()
    
    def setup(self, dispatcher):
        self.load()
        handler = CommandHandler('clearmeeting', self.handle_clearmeeting, Filters.command)
        dispatcher.add_handler(handler)
        handler = CommandHandler('nextmeeting', self.handle_nextmeeting, Filters.command)
        dispatcher.add_handler(handler)        
        self.cmd_setnextmeeting.setup(dispatcher)

def setup_handler(dispatcher):
    print("Setup meeting commands");
    instance = MeetingManager()
    instance.setup(dispatcher)
