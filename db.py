from model import Base, Entity, Message
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class BotDatabase:

    def connect(self, driver, database):
        self.engine = create_engine(driver + '://' + database)
        Base.metadata.create_all(self.engine, checkfirst=True)
        Base.metadata.bind = self.engine
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()
        self.session.commit()

    def add_message(self, message):
        self.session.add(message)
        self.session.commit()

    def add_entity(self, entity):
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
