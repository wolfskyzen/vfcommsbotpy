#!/usr/bin/python
from telegram import Chat
from telegram.ext import CommandHandler
from telegram.ext import Filters

def handle_about(bot, update):
    message = """VancouFur Staff Communications Bot
Version 2.0
Created by Zen using the Python Telegram Bot API.
https://github.com/wolfskyzen/vfcommsbotpy"""
    bot.sendMessage(chat_id=update.message.chat_id, text=message, reply_to_message_id=update.message.message_id)

def setup_handler(dispatcher):
    handler = CommandHandler('about', handle_about, Filters.command)
    dispatcher.add_handler(handler);
