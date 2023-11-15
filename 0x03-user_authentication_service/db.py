#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, create_session
from sqlalchemy.orm.session import Session
from typing import TypeVar
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base
from user import User
import bcrypt


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            """ DBSession = create_session(bind=self._engine) """
            """ self.__session = DBSession() """
            self.__session = create_session(bind=self._engine)
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> TypeVar('User'):
        """ The function that will add a user to db """
        hashed_pass = bcrypt.hashpw(hashed_password.encode(), bcrypt.gensalt())
        user = User(email=email, hashed_password=hashed_pass)
        if self.__session is None:
            """ DBSession = create_session(bind=self._engine)
            session = DBSession() """
            session = create_session(bind=self._engine)
        else:
            session = self.__session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **obj):
        """ This function searches for a user """
        searchable = ['id', 'email']
        if not obj:
            raise InvalidRequestError
        else:
            for key in obj.keys():
                if key not in searchable:
                    raise InvalidRequestError
        if not self.__session:
            self._session
        res = self.__session.query(User).filter_by(**obj).first()
        if not res:
            raise NoResultFound
        return res

    def update_user(self, user_id, **data):
        """ The function for updating a specific user """
        user = self.find_user_by(id=user_id)
        """ Validate to see if key exists """
        if user:
            updatables = [
                "email", "session_id", 'hashed_password', 'reset_token'
            ]
            for key in data.keys():
                if key not in updatables:
                    raise ValueError(f"The key {key} does is can not be added")
                setattr(user, key, data[key])
            self._session.commit()
        else:
            raise ValueError("No user to be updated")
