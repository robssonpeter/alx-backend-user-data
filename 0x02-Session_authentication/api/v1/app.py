#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = getenv('AUTH_TYPE', 'basic_auth')
if auth:
    if auth == 'auth':
        from api.v1.auth.auth import Auth
        auth = Auth()
    elif auth == 'session_auth':
        from api.v1.auth.session_auth import SessionAuth
        auth = SessionAuth()
    else:
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()


@app.before_request
def requiring_auth():
    """ This function checks if a give request needs auth """
    path = request.path
    exceptionals = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/',
    ]
    if auth:
        require_auth = auth.require_auth(path, exceptionals)
        header = auth.authorization_header(request)
        current_user = auth.current_user(request)
        cookie = auth.session_cookie(request)
        request.current_user = current_user

        if isinstance(auth, SessionAuth):
            if cookie is None and header is None:
                abort(401)
        if require_auth:
            if header is None:
                abort(401)
            elif current_user is None:
                abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """ The handle for restricted content """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
