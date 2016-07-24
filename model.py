from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Message(Base):
     __tablename__ = 'messages'
     from_id = Column(BigInteger, ForeignKey('entities.id'), nullable=False)
     to_id = Column(BigInteger, ForeignKey('entities.id'), nullable=False)
     text = Column(Text, nullable=False)
     date = Column(Integer, nullable=False)
     message_id = Column(BigInteger, primary_key=True, nullable=False)

class Entity(Base):
     __tablename__ = 'entities'
     id = Column(BigInteger, primary_key=True)
     is_group = Column(Boolean, nullable=False)
     username = Column(String(255), nullable=True)
     first_name = Column(String(255), nullable=True)
     last_name = Column(String(255), nullable=True)
     title = Column(String(255), nullable=True)
     is_being_tracked = Column(Boolean, default=True, nullable=False)
