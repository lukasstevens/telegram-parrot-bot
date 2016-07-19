def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hello there.")

def parrot(bot, update, args):
    bot.sendMessage(chat_id=update.message.chat_id, text=args)
