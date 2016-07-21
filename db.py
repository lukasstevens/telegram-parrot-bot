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

    def add_group(self, group_id, title):
        group = Entity(id=group_id, title=title, is_group=True)
        self.session.add(group)
        self.session.commit()

    def add_user(self, user_id, username, first_name, last_name=None):
        user = Entity(id=user_id, is_group=False, first_name=first_name, last_name=last_name, username=username)
        self.session.add(user)
        self.session.commit()




