#!/usr/bin/env python

import argparse
from bottle import request, response, route, run, static_file, template
import sys

USERS = {
    'abc': 'Bob',
    'def': 'Fred'
}

COOKIE_PATH='/'
TOKEN='token'

@route('/')
def home():
    cookie_token = request.get_cookie(TOKEN)
    if cookie_token:
        logged_in_user = USERS[cookie_token]
        return template('main', name=logged_in_user)
    else:
        return template('message', message="Not logged in",
                        logout_link=False,
                        start_link=False)

@route('/login/:token')
def login(token):
    cookie_token = request.get_cookie(TOKEN)
    if cookie_token:
        logged_in_user = USERS[cookie_token]
        return template('message',
                        message=("Already logged in as %s" % logged_in_user),
                        logout_link=True,
                        start_link=True)
    elif USERS.has_key(token):
        user = USERS[token]
        response.set_cookie('token', token, path=COOKIE_PATH)
        return template('message',
                         message=("Logged in as %s" % user),
                         logout_link=True,
                         start_link=True)
    else:
        return template('message',
                        message="Invalid token",
                        logout_link=False,
                        start_link=False)

@route('/logout')
def logout():
    response.delete_cookie(TOKEN, path=COOKIE_PATH)
    return template('message',
                    message="Logged out",
                    logout_link=False,
                    start_link=False)

@route('/static/<filepath:path>')
def static(filepath):
    return static_file(filepath, root='static/')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', default='127.0.0.1',
                        help='The address on which to listen')
    parser.add_argument('-p', '--port', default=8080,
                        help='The port on which to listen')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Run in debug mode')
    args = parser.parse_args(sys.argv[1:])
    run(host=args.address, port=args.port, debug=args.debug)
