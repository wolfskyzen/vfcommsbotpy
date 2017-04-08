#!/usr/bin/python
from comms import users
from telegram import Chat
from telegram.ext import CommandHandler
from telegram.ext import Filters

BASIC_HELP = """Valid commands for the VancouFur Communication Bot

/about - Show information about this bot.
/broadcast - Send a message to all VF Staff chatrooms at the same time. (Must be sent as a Direct Message.)
/help - Show this list of commands
/meetinglink - Gives the active meeting online link, when a staff meeting is happening.
/nextmeeting - Displays the date, time and location of the next staff meeting."""

ADMIN_HELP = """

Admin commands. If you get this message, you can use these commands. Must be sent via direct message.

/addgroup - Adds a group to the internal list for broadcast targets. Send this as a group message and use /listgroups to see the results in DM.
/adminadd - Adds a user to the admin list. Must include an @ mention of the user to add. Target user must also message the bot with /noticeme to get added to the internal userlist.
/adminremove - Adds a user to the admin list. Must include an @ mention of the user to add.
/clearmeetinglink - Clears the current remote meeting link.
/listgroups - List all the known groups setup with /addgroup.
/setmeetinglink - Set a valid weblink for remote meeting connection. Will broadcast to all groups when changed.
/setnextmeeting - Set the date, time and location of the next meeting. Will broadcast to all groups when changed.
/userlist - Lists the usernames of all noticed users, and which ones are admins.
/whois - A test command that just replies to you."""

def handle_help(bot, update):
    if update.message.chat.type == Chat.PRIVATE:
        message = BASIC_HELP
        if users.is_admin(update.message.from_user.id):
            message = message + ADMIN_HELP
        bot.sendMessage(chat_id=update.message.chat_id, text=message)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text=BASIC_HELP, reply_to_message_id=update.message.message_id)

def setup_handler(dispatcher):
    handler = CommandHandler('help', handle_help, Filters.command)
    dispatcher.add_handler(handler);
