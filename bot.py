#!/usr/bin/env python3

import configparser
from telegram.ext import Updater, CommandHandler
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Read the API key
config = configparser.ConfigParser()
config.read('api_key.ini')
api_key = config.get('api_key', 'api_key')

updater = Updater(token=api_key)
dispatcher = updater.dispatcher

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hello there.")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()
