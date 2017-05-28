#!/usr/bin/python
import json
import os
import sys
from telegram import Chat
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler

class Group:
    allowed = False
    id = 0
    title = None

    def __repr__(self):
        return "{0} {1} {2}".format(self.id, self.title, self.allowed)

    def from_chat(chat, allowed):
        group = Group()
        group.allowed = allowed
        group.id = chat.id
        group.title = chat.title
        return group

    def from_json(json):
        group = Group()
        group.allowed = json["allowed"]
        group.id = json["id"]
        group.title = json["title"]
        return group

    def to_json(self):
        obj = { "id": self.id, "title": self.title, "allowed": self.allowed }
        return obj

class _BroadcastCommand:
    users = list()
    broadcaster = None
    
    WAITING = range(1)

    def __init__(self, broadcaster):
        self.broadcaster = broadcaster

    def handle_broadcast(self, bot, update):
        if update.message.chat.type != Chat.PRIVATE:            
            return ConversationHandler.END
        if not self.broadcaster.can_broadcast():
            message = "There are no groups setup to broadcast in. Please enable broadcasting in a group before using this command."
            bot.sendMessage(update.message.chat_id, message)
            return ConversationHandler.END
        user_id = update.message.from_user.id
        if user_id in self.users:
            return ConversationHandler.END
        self.users.append(user_id)
        message = "Please tell me the message you wish to broadcast to ALL VF Staff chatrooms. Or message me with /cancel to stop the broadcast."
        bot.sendMessage(update.message.chat_id, message)
        return _BroadcastCommand.WAITING

    def handle_cancel(self, bot, update):
        if update.message.chat.type != Chat.PRIVATE:
            return ConversationHandler.END
        user_id = update.message.from_user.id
        if user_id in self.users:
            self.users.remove(user_id)
            message = "Your message broadcast has been cancelled."
            bot.sendMessage(update.message.chat_id, message)
        return ConversationHandler.END

    def handle_message(self, bot, update):
        if update.message.chat.type != Chat.PRIVATE:
            return ConversationHandler.END
        user_id = update.message.from_user.id
        if user_id in self.users:
            self.users.remove(user_id)
            self.broadcaster.broadcast(bot, update.message.from_user, update.message.text)
            message = "Your message has been broadcast to ALL VF Staff chatrooms."
            bot.sendMessage(update.message.chat_id, message)
        return ConversationHandler.END

    def setup(self, dispatcher):
        handler = ConversationHandler(
            entry_points=[CommandHandler('broadcast', self.handle_broadcast, Filters.command)],
            
            states={
                _BroadcastCommand.WAITING: [MessageHandler(Filters.text, self.handle_message)],
            },
            
            fallbacks=[CommandHandler('cancel', self.handle_cancel, Filters.command)]
        )
        dispatcher.add_handler(handler)

"""
TODO: Build these two classes to use the inline commands to enable/disable groups from the broadcast list
TODO: Abstract this into a GroupManager that the broadcast command can communicate with

class _DisableBroadcastCommand:

class _EnableBroadcastCommand:
"""

class Broadcaster:
    FILE_NAME = 'var/GROUPS'

    groups = dict()

    cmd_broadcast = None

    def __init__(self):
        self.cmd_broadcast = _BroadcastCommand(self)

    def broadcast(self, bot, user, message):
        if not self.groups:
            return
        try:
            final_message = message;
            if user is not None:
                final_message = "Message from @{0}:\n\n".format(user.username) + message
            for k, v in self.groups.items():
                if v.allowed:
                    bot.sendMessage(v.id, final_message)
        except:
            print(sys.exc_info())
            
    def can_broadcast(self):
        if not self.groups:
            return False
        for k, v in self.groups.items():
            if v.allowed:
                return True
        return False

    def handle_addgroup(self, bot, update):
        if update.message.chat.type == Chat.PRIVATE:
            return
        group_id = update.message.chat.id
        if not self.groups or group_id not in self.groups:
            self.groups[group_id] = Group.from_chat(chat, True)
            self.save()
        else:
            print("Group '{0}' already added".format(update.message.chat.title))
            
    def handle_listgroups(self, bot, update):
        if update.message.chat.type != Chat.PRIVATE:
            return
        message = None
        if not self.groups:
            message = "There are no groups setup to broadcast in. Use /addgroup, in that group, to add it to the broadcast list."
        else:
            message = "Group Title (Broadcasting)\n"
            for k, v in self.groups.items():
                message += "\n{0} ({1})".format(v.title, str(v.allowed))
        if not message == None:
            bot.sendMessage(update.message.from_user.id, message)    

    def load(self):
        if os.path.isfile(self.FILE_NAME) == False:
            return
        root = None
        with open(self.FILE_NAME, 'r') as file:
            root = json.load(file)
            file.close()
        for k, v in root.items():
            group = Group.from_json(v)
            self.groups[group.id] = group

    def save(self):
        root = {}
        for k, v in self.groups.items():
            root[k] = v.to_json()
        with open(self.FILE_NAME, 'w') as file:
            json.dump(root, file, indent=4)
            file.close()

    def setup(self, dispatcher):
        self.load()
        handler = CommandHandler('addgroup', self.handle_addgroup, Filters.command)
        dispatcher.add_handler(handler);
        handler = CommandHandler('listgroups', self.handle_listgroups, Filters.command)
        dispatcher.add_handler(handler);        
        self.cmd_broadcast.setup(dispatcher)

global instance

def broadcast(bot, message):
    global instance
    if instance is not None:
        instance.broadcast(bot, None, message)

def setup_handler(dispatcher):
    print("Setup broadcast commands");
    global instance
    instance = Broadcaster()
    instance.setup(dispatcher)
