#!/usr/bin/env python3

import configparser
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.messagehandler import Filters
from sqlalchemy import create_engine
from db import BotDatabase
import logging
from parrotbot import ParrotBot

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()

    # Read the API key
    config = configparser.ConfigParser()
    config.read('api_key.ini')
    api_key = config.get('api_key', 'api_key')

    updater = Updater(token=api_key)
    dispatcher = updater.dispatcher

    database = BotDatabase()
    database.connect('sqlite', '/db.sqlite3')

    bot = ParrotBot(database)

    dispatcher.add_handler(CommandHandler('start', bot.start))
    dispatcher.add_handler(CommandHandler('parrot', bot.parrot, pass_args=True))
    dispatcher.add_handler(MessageHandler([Filters.text], bot.new_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
