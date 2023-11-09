#!/usr/bin/env python3
""" The module containing basic auth class """
from api.v1.auth.auth import Auth
import base64
import binascii
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ The class BasicAuth for authentication"""
    def extract_base64_authorization_header(self, auth_header: str) -> str:
        """ The function to extract auth value from header """
        if auth_header is None:
            return None
        if not isinstance(auth_header, str):
            return None
        if auth_header[:6] != "Basic ":
            return None
        return auth_header[6:]

    def decode_base64_authorization_header(self, b64_auth_header: str) -> str:
        """ The function to decode base64 text """
        if b64_auth_header is None:
            return None
        if not isinstance(b64_auth_header, str):
            return None
        else:
            try:
                header = b64_auth_header.encode()
                decoded = base64.b64decode(header).decode('utf-8')
                return decoded
            except UnicodeDecodeError:
                return None
            except binascii.Error:
                return None

    def extract_user_credentials(self, dec_b64_auth_header: str) -> (str, str):
        """ Function to extract credentials """
        if dec_b64_auth_header is None:
            return None, None
        if not isinstance(dec_b64_auth_header, str):
            return None, None
        if ':' not in dec_b64_auth_header:
            return None, None
        lst = dec_b64_auth_header.split(':')
        if (len(lst) > 2):
            pass_arr = lst[1:]
            return (lst[0], ':'.join(pass_arr))
        return tuple(dec_b64_auth_header.split(':'))

    def user_object_from_credentials(self, e: str, p: str) -> TypeVar('User'):
        """ The function for creating the user object """
        if e is None or not isinstance(e, str):
            return None
        if p is None or not isinstance(p, str):
            return None
        searched = User.search({'email': e})
        if len(searched):
            for usr in searched:
                if(usr.is_valid_password(p)):
                    return usr
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get the current user of this request """
        auth_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(base64_header)
        cred = self.extract_user_credentials(decoded_header)
        cred_obj = self.user_object_from_credentials(cred[0], cred[1])
        return cred_obj
