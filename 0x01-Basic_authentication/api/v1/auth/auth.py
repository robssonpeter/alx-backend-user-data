#!/usr/bin/env python3
""" The module containing the class auth for authentication"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ The class auth for returning all the routes requireding auth """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ The function for checking routes requiring authentication """
        starred_paths = [x for x in excluded_paths if '*' in x]
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path[-1] != '/':
            path = path+'/'
            return path not in excluded_paths
        else:
            for starred in starred_paths:
                if path in starred:
                    return False
        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """ The function to handle authorization header content """
        if request is None:
            return None
        elif 'Authorization' in request.headers.keys():
            return request.headers['Authorization']
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ The method that will return the current user logged """
        return None
