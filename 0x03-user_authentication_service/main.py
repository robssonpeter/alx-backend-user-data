#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

#auth.register_user(email, password)

print(auth.get_user_from_session_id(session_id='0486b15b-aefa-44e3-a6a3-478e085b4843'))