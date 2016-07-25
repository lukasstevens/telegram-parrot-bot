from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Base, Entity, Message

class BotDatabase:

    def connect(self, driver, database):
        self.engine = create_engine(driver + '://' + database)
        # Create only if not exists
        Base.metadata.create_all(self.engine, checkfirst=True)
        Base.metadata.bind = self.engine
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()
        self.session.commit()

    def add_message(self, message):
        self.session.add(message)
        self.session.commit()

    def add_entity(self, entity):
        # Columns which have changed are updated
        self.session.merge(entity)
        self.session.commit()

    def get_entities(self, query=None):
        if query is not None:
            return self.session.query(Entity, query)
        else:
            return self.session.query(Entity)

    def get_messages(self, query=None):
        if query is not None:
            return self.session.query(Message, query)
        else:
            return self.session.query(Message)

    def delete_messages(self, predicate):
        messages = self.session.query(Message).filter(predicate).all()
        for message in messages:
            self.session.delete(message)
        self.session.commit()

    def __del__(self):
        self.session.close()
