from model import Message, Entity

class ParrotBot:
    def __init__(self, bot_database):
        self._bot_database = bot_database

    def start(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Hello there.")

    def parrot(self, bot, update, args):
        bot.sendMessage(chat_id=update.message.chat_id, text=args)

    def new_message(self, bot, update):
        up_msg = update.message
        from_id = up_msg.from_user.id
        to_id = up_msg.chat.id
        text = up_msg.text
        date = up_msg.date
        message_id = up_msg.message_id
        message = Message(from_id=from_id, to_id=to_id, text=text, date=date, message_id=message_id)
        self._bot_database.add_message(message)
        self._new_entity(update.message.from_user)
        self._new_entity(update.message.chat)

    def _new_entity(self, entity):
        if entity.type == 'group':
            group = Entity(id=entity.id, is_group=True, title=entity.title)
            self._bot_database.add_entity(group)
        else:
            username=entity.username
            first_name=entity.first_name
            last_name=entity.last_name
            user = Entity(id=entity.id, is_group=False, username=username, first_name=first_name, last_name=last_name)
            self._bot_database.add_entity(user)
