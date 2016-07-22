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

    def disconnect(self):
        self.session.close()

    def add_message(self, message):
        self.session.add(message)
        self.session.commit()

    def add_entity(self, entity):
        self.session.merge(entity)
        self.session.commit()

    def get_entities(self, predicate):
        return self.session.query(Entity).filter(predicate).all()

    def get_entity(self, predicate):
        return self.session.query(Entity).filter(predicate).one_or_none()

    def get_messages(self, predicate):
        return self.session.query(Message).filter(predicate).all()

    def get_message(self, predicate):
        return self.session.query(Message).filter(predicate).one_or_none()


