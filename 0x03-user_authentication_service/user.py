#!/usr/bin/env python3
""" The module containing the user model"""
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """ The model user that connects to database """
    __tablename__ = 'users'
    id = Column('id', Integer(), autoincrement=True, primary_key=True)
    email = Column('email', String(250), nullable=False)
    hashed_password = Column('hash_password', String(250), nullable=False)
    session_id = Column('session_id', String(250), nullable=True)
    reset_token = Column('reset_token', String(250), nullable=True)
