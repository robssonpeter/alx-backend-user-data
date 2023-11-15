#!/usr/bin/env python3
""" The module containing the user model"""
from sqlalchemy import Column, Integer, String, create_engine, INTEGER
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('mysql://parker:07570237@localhost/sqlalchemy')

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column('id', Integer(), autoincrement=True, primary_key=True)
    email = Column('email', String(250), nullable=False)
    hashed_password = Column('hash_password', String(250), nullable=False)
    session_id = Column('session_id', String(250), nullable=True)
    reset_token = Column('reset_token', String(250), nullable=True)
