#!/usr/bin/env python3
""" The module that will contain session authentication """
from api.v1.auth.auth import Auth
from models.user import User
from flask import session
import uuid


class SessionAuth(Auth):
    """ The class for session authentication """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ The function for creating a session """
        if user_id is None:
            return None
        elif not isinstance(user_id, str):
            return None
        else:
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Get the user id of a specific session """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ a method overload for returning the current user """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        result = User.search({'id': user_id})
        """ print(Auth.authorization_header(request))
        print(Auth.session_cookie(request)) """
        if len(result):
            return result[0]
        return None

    def destroy_session(self, request=None):
        """ The method for logging out of the application """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if request is None:
            return False