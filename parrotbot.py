import itertools
import logging
import re
from random import choice
from sqlalchemy import func, and_

from model import Message, Entity

class ParrotBot:
    def __init__(self, bot_database):
        self._bot_database = bot_database

    def parrot(self, bot, update, args):
        # Since the user id is unique there can be only one user
        user = self._bot_database.get_entities().filter(Entity.username == args[0]).one()
        # Get messages from this user in this chat
        messages = self._bot_database.get_messages().\
                filter(and_(Message.from_id == user.id, Message.to_id == update.message.chat.id)).all()
        # Check if user has send a message yet
        if len(messages) > 0:
            chain = {}

            def get_text(message): return message.text
            def split_sentence(string): return re.split('(\?|!|\.|,)', string)
            def strip(string_list): return list(map(str.split, string_list))
            def not_empty(string_list): return len(string_list) != 0
            messages_text = map(get_text, messages)
            # Split around terminators then, strip the strings and remove empty lists
            sentences = list(filter(not_empty, map(strip, map(split_sentence, messages_text))))

            for sentence in sentences:
                def append_none(string):
                    if re.match('[\?\.!]', string) is not None:
                        return [string, None]
                    else:
                        return [string]
                sentence = list(itertools.chain.from_iterable(map(append_none, sentence)))
                sentence.append(None)

            def first_word(string_list): return string_list[0]
            first_words = list(map(first_word, sentences))

            for sentence in sentences:
                last_word = None
                for word in sentence:
                    try:
                        chain[last_word].append(word)
                    except KeyError:
                        chain[last_word] = [word]
                    last_word = word

            curr_word = choice(first_words)
            message = curr_word
            building_message = True
            while building_message:
                next_word_list = chain[curr_word]
                next_word = choice(next_word_list)
                if next_word is None:
                    # 50/50 chance that message is finished after a terminating symbol (?,!,.)
                    if choice([True, False]):
                        # Begin new sentence
                        next_word = choice(first_words)
                    else:
                        # Finished with building message
                        building_message
                else:
                    message += ' ' + next_word
                curr_word = next_word
            bot.sendMessage(chat_id=update.message.chat_id, text=message)


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
