import logging
from sqlalchemy import func

from model import Message, Entity

class ParrotBot:
    def __init__(self, bot_database):
        self._bot_database = bot_database

    def start(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Hello")

    def parrot(self, bot, update, args):
        # Since the user id is unique there can be only one user
        user = self._bot_database.get_entities().filter(Entity.username == args[0]).one()
        # Get last message from this user
        message = self._bot_database.get_messages().filter(Message.from_id == user.id).order_by(Message.date.desc()).first( )
        # Check if user has send a message yet
        if message is not None:
            bot.sendMessage(chat_id=update.message.chat_id, text=message.text)

    def forget(self, bot, update):
        user_id = update.message.from_user.id
        self._bot_database.delete_messages(Message.from_id == user_id)
        message = 'All your messages have been deleted. ' \
            'To also stop further tracking use the set_tracking command.'
        bot.sendMessage(chat_id=update.message.chat_id, text=message)

    def set_tracking(self, bot, update, args):
        # Parse input first
        tracking_status = None
        if len(args) == 1:
            if args[0].lower() == 'true':
                tracking_status = True
            elif args[0].lower() == 'false':
                tracking_status = False
        # If input is correct update tracking status
        if tracking_status is not None:
            entity = self._bot_database.get_entities().filter(Entity.id == update.message.from_user.id).one()
            entity.is_being_tracked = tracking_status
            self._bot_database.add_entity(entity)
            message = 'Your tracking status is now: ' + str(tracking_status) + '. ' \
                'To delete all messages use the forget command.'
            bot.sendMessage(chat_id=update.message.chat_id, text=message)

    def new_message(self, bot, update):
        up_msg = update.message
        from_id = up_msg.from_user.id
        to_id = up_msg.chat.id
        text = up_msg.text
        date = up_msg.date
        message_id = up_msg.message_id

        # Update/Add the entities which are part of this update
        self._new_entity(update.message.from_user)
        self._new_entity(update.message.chat)

        # Get sender of the message in this update
        entity = self._bot_database.get_entities().filter(Entity.id == from_id).one()
        # Log message if tracking status is True
        if entity.is_being_tracked:
            message = Message(from_id=from_id, to_id=to_id, text=text, date=date, message_id=message_id)
            self._bot_database.add_message(message)


    def _new_entity(self, entity):
        # Update/Add entity according to database model
        if entity.type == 'group':
            group = Entity(id=entity.id, is_group=True, title=entity.title)
            self._bot_database.add_entity(group)
        else:

            username=entity.username
            first_name=entity.first_name
            last_name=entity.last_name
            user = Entity(id=entity.id, is_group=False, username=username, first_name=first_name, last_name=last_name)
            self._bot_database.add_entity(user)
