#!/usr/bin/env python3
""" The simple flask app for project auth """
from flask import Flask
from flask import jsonify
from flask import request
from flask import abort
from flask import make_response
from flask import redirect
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound


AUTH = Auth()

app = Flask(__name__)


@app.route('/')
def home():
    """ The homepage of the application """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """ The users registration handling route """
    email = request.form.get('email')
    password = request.form.get('password')
    """ check if user exists """
    db = AUTH.db
    try:
        db.find_user_by(email=email)
        return jsonify({"message": "email already registered"})
    except NoResultFound:
        """ Create a new user """
        db.add_user(email, password)
        return jsonify({"email": email, "message": "user created"})


@app.route('/sessions', methods=['POST', 'DELETE'])
def login():
    """ The route for loging the user in """
    email = request.form.get('email')
    password = request.form.get('password')
    """ Call the authetication function """
    authentic = AUTH.valid_login(email, password)
    if not authentic:
        abort(401)
    else:
        logged = AUTH.create_session(email)
        if logged:
            response = {"email": email, "message": "logged in"}
            if not isinstance(logged, str):
                logged = str(logged)
            resp = make_response(jsonify(response))
            resp.set_cookie('session_id', logged)
            return resp
        else:
            return jsonify({})


@app.route('/sessions', methods=['DELETE'])
def logout():
    """ The logout route """
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        resp = make_response('cookie removed')
        if user:
            AUTH.destroy_session(user.id)
            resp.set_cookie('session_id', '', max_age=0)
        else:
            print('you are ')
            return resp, 403
    return redirect('/')


@app.route('/profile')
def profile():
    """ The route for displaying user profile """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        return abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
