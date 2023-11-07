#!/usr/bin/env python3
""" The module containing basic auth class """
from api.v1.auth.auth import Auth
import base64
import binascii
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ The class BasicAuth for authentication"""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ The function to extract auth value from header """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if authorization_header[:6] != "Basic ":
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """ The function to decode base64 text """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        else:
            try:
                header = base64_authorization_header.encode()
                decoded = base64.b64decode(header).decode('utf-8')
                return decoded
            except UnicodeDecodeError:
                return None
            except binascii.Error:
                return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """ Function to extract credentials """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        lst = decoded_base64_authorization_header.split(':')
        if (len(lst) > 2):
            pass_arr = lst[1:]
            return (lst[0], ':'.join(pass_arr))
        return tuple(decoded_base64_authorization_header.split(':'))

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ The function for creating the user object """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        searched = User.search({'email': user_email})
        if len(searched):
            return searched[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get the current user of this request """
        auth_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(base64_header)
        cred = self.extract_user_credentials(decoded_header)
        cred_obj = self.user_object_from_credentials(cred[0], cred[1])
        return cred_obj
