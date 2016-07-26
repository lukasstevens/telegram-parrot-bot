import configparser
import logging
from sqlalchemy import create_engine
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.messagehandler import Filters

from db import BotDatabase
from parrotbot import ParrotBot

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()

    # Read the API key
    config = configparser.ConfigParser()
    config.read('api_key.ini')
    # Section and key
    api_key = config.get('api_key', 'api_key')

    updater = Updater(token=api_key)
    dispatcher = updater.dispatcher

    database = BotDatabase()
    database.connect('sqlite', '/db.sqlite3')

    bot = ParrotBot(database)

    dispatcher.add_handler(CommandHandler('parrot', bot.parrot, pass_args=True))
    # Only handle text messages, no media content
    dispatcher.add_handler(MessageHandler([Filters.text], bot.new_message))
    dispatcher.add_handler(CommandHandler('forget', bot.forget))
    dispatcher.add_handler(CommandHandler('set_tracking', bot.set_tracking, pass_args=True))

    updater.start_polling()
    # Idle to correctly handle KeyboardInterrupt and other things
    updater.idle()

if __name__ == '__main__':
    main()
