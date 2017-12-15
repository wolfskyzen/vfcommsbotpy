#!/usr/bin/python
import json
import os
import sys
from telegram import Chat
from telegram import MessageEntity
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters

class User:
    admin = False
    id = 0
    username = None
    
    def __repr__(self):
        return "{0} {1} {2}".format(self.id, self.username, self.admin)
    
    def from_chat(user, admin):
        new_user = User()
        new_user.admin = admin
        new_user.id = user.id
        new_user.username = user.username
        return new_user

    def from_json(json):
        new_user = User()
        new_user.admin = json["admin"]
        new_user.id = json["id"]
        new_user.username = json["username"]
        return new_user

    def to_json(self):
        obj = { "id": self.id, "username": self.username, "admin": self.admin }
        return obj

class UserManager:
    FILE_NAME = 'var/USERS'
    
    users = dict()
    
    def can_remove_admin(self):
        if None is self.users:
            return False
        num_admins = 0
        for k, v in self.users.items():
            if v.admin:
                num_admins += 1
        return bool(num_admins > 1)
    
    def change_admin_status(self, username, new_status):
        found = False
        changed = False
        if None is username or len(username) == 0:
            return found, changed
        searchname = ""
        if username.startswith("@"):
            searchname = username[1:].lower()
        else:
            searchname = username.lower()
        for k, v in self.users.items():
            if v.username.lower() == searchname:
                changed = bool(v.admin != new_status)
                if changed:
                    v.admin = new_status
                    self.save()
                found = True
                return found, changed
        return found, changed
    
    def find_mentioned_user(message):
        mentions = message.parse_entities(MessageEntity.MENTION)
        if mentions:
            for k, v in mentions.items():
                return v
        return None
    
    def handle_adminadd(self, bot, update):
        if update.message.chat.type != Chat.PRIVATE:
            return
        user_id = update.message.from_user.id
        if not self.is_admin(user_id):
            return
        message = ""
        username = UserManager.find_mentioned_user(update.message)
        if not username:
            message = "Unable to find a username to add. Please include a username with the @ mention format."
        else:
            found, changed = self.change_admin_status(username, True)
            if not found:
                message = "Unable to find {0} in the userlist. Please get them to direct message the bot with /noticeme first."
            elif not changed:
                message = "{0} is already an admin."
            else:
                message = "{0} is now an admin!"
            message = message.format(username)
        bot.sendMessage(update.message.from_user.id, message)

    def handle_adminremove(self, bot, update):
        if update.message.chat.type != Chat.PRIVATE:
            return
        user_id = update.message.from_user.id
        if not self.is_admin(user_id):
            return
        if not self.can_remove_admin():
            message = "You must have at least one admin for the bot."
            bot.sendMessage(update.message.from_user.id, message)
            return
        message = ""
        username = UserManager.find_mentioned_user(update.message)
        if not username:
            message = "Unable to find a username to remove. Please include a username with the @ mention format."
        else:
            found, changed = self.change_admin_status(username, False)
            if not found:
                message = "Unable to find {0} in the userlist. Please get them to direct message the bot with /noticeme first."
            elif not changed:
                message = "{0} is not an admin."
            else:
                message = "{0} is no longer an admin!"
            message = message.format(username)
        bot.sendMessage(update.message.from_user.id, message)

    def handle_noticeme(self, bot, update):
        if update.message.chat.type != Chat.PRIVATE:
            return
        user_id = update.message.from_user.id
        message = ""
        if not self.users or user_id not in self.users:
            admin = False
            if not self.users:
                # If there are no users, at all, make the first one an admin
                admin = True
                message = "You are senpai now!"
            else:
                message = "Senpai has noticed you."
            user = User.from_chat(update.message.from_user, admin)
            self.users[user.id] = user
            self.save()
        else:
            user = self.users[user_id]
            curr_username = update.message.from_user.username
            if user.username != curr_username:
                message = "Senpai noticed you again"
                user.username = curr_username
                self.save()
            else:
                message = "Senpai already noticed you."
        bot.sendMessage(update.message.from_user.id, message)
        
    def handle_userlist(self, bot, update):
        if update.message.chat.type != Chat.PRIVATE:
            return
        user_id = update.message.from_user.id
        if not self.is_admin(user_id):
            return
        message = ""
        if not self.users:
            message = "No users are setup"
        else:
            admins = list()
            users = list()
            for k, v in self.users.items():
                if v.admin:
                    admins.append(v.username)
                else:
                    users.append(v.username)
            if admins:
                message = message + "Admins:"
                for name in admins:
                    message = message + "\n@" + name
            if users:
                message = message + "\nNoticed users:"
                for name in users:
                    message = message + "\n@" + name
        if not message == None:
            bot.sendMessage(update.message.from_user.id, message)
            
    def is_admin(self, id):
        return bool(self.users and id in self.users)    
    
    def load(self):
        if os.path.isfile(self.FILE_NAME) == False:
            return
        root = None
        with open(self.FILE_NAME, 'r') as file:
            root = json.load(file)
            file.close()
        for k, v in root.items():
            user = User.from_json(v)
            self.users[user.id] = user
        
    def save(self):
        root = {}
        for k, v in self.users.items():
            root[k] = v.to_json()
        with open(self.FILE_NAME, 'w') as file:
            json.dump(root, file, indent=4)
            file.close()
    
    def setup(self, dispatcher):
        self.load()
        handler = CommandHandler('adminadd', self.handle_adminadd, Filters.command)
        dispatcher.add_handler(handler)
        handler = CommandHandler('adminremove', self.handle_adminremove, Filters.command)
        dispatcher.add_handler(handler)
        handler = CommandHandler('noticeme', self.handle_noticeme, Filters.command)
        dispatcher.add_handler(handler)
        handler = CommandHandler('userlist', self.handle_userlist, Filters.command)
        dispatcher.add_handler(handler)

global instance

def is_admin(id):
    global instance
    return instance.is_admin(id)

def setup_handler(dispatcher):
    print("Setup user commands");
    global instance
    instance = UserManager()
    instance.setup(dispatcher)
