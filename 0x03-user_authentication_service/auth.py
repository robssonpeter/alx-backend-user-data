#!/usr/bin/env python3
""" The module that will contain pass hashing function """
import bcrypt
from db import DB
from typing import TypeVar
from user import User
from sqlalchemy.exc import NoResultFound


def _hash_password(password) -> bytes:
    """the function to create a hashed password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """ The function for registering a user """

        try:
            """ check if the user already exists """
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            if not isinstance(password, bytes):
                hashed_pass = _hash_password(password).decode()
            else:
                hashed_pass = password.decode()
            return self._db.add_user(email, hashed_pass)
