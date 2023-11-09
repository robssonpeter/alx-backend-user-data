#!/usr/bin/env python3
""" The module that for I dont know what """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ The place where the user attempt to login """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    elif not password:
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    else:
        if not user[0].is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
        else:
            from api.v1.app import auth
            session_id = auth.create_session(user[0].id)
            resp = jsonify(user[0].to_json())
            session_name = os.getenv('SESSION_NAME', '')
            resp.set_cookie(session_name, session_id)
            return resp
