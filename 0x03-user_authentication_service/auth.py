#!/usr/bin/env python3
""" The module that will contain pass hashing function """
import bcrypt
from db import DB
from typing import TypeVar
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password) -> bytes:
    """the function to create a hashed password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ The function to generate user id """
    return uuid.uuid4().__repr__


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    @property
    def db(self):
        """ The property db function """
        return self._db

    @db.getter
    def db(self) -> DB:
        """ Get the db information """
        return self._db

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """ The function for registering a user """

        try:
            """ check if the user already exists """
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            return self._db.add_user(email, password)

    def valid_login(self, email: str, password: str) -> bool:
        """ The function to validate the login details """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ The function to create a session for user """
        """ user = self._db.find_user_by(email=email)
        uid = uuid.uuid4()
        setattr(user, 'session_id', uid)
        self._db.update_user(user.id, session_id=uid)
        return uid """
        try:
            user = self._db.find_user_by(email=email)
            uid = uuid.uuid4()
            setattr(user, 'session_id', str(uid))
            self._db.update_user(user.id, session_id=str(uid))
            return str(uid)
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id) -> TypeVar('user'):
        """ Search user by using session_id """
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user.session_id is None:
                return None
            else:
                return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id) -> None:
        """ Destroy session of a user """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
            return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ The function for getting the password token """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                token = str(uuid.uuid4())
                self._db.update_user(user.id, reset_token=token)
                return token
        except NoResultFound:
            raise ValueError('User does not exist')

    def update_password(self, reset_token: str, password: str) -> None:
        """ The function for updating the new password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if not user:
                raise ValueError('Could not find user')
            h_pass = str(_hash_password(password))
            self._db.update_user(user.id, password=h_pass, reset_token=None)
        except NoResultFound:
            raise ValueError('Could not find user')
