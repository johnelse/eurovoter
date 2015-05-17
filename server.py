#!/usr/bin/env python

import argparse
from bottle import request, response, route, run, static_file, template
import sqlite3
import sys

COOKIE_PATH='/'
TOKEN='token'

db_path=""

def get_voter(token):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM voters WHERE token = '%s'" % token)
    result = cursor.fetchone()
    conn.close()
    if result:
        voter_id, name, _ = result
        return (voter_id, name)
    else:
        return None

@route('/')
def home():
    cookie_token = request.get_cookie(TOKEN)
    if cookie_token:
        _, name = get_voter(cookie_token)
        return template('main', name=name)
    else:
        return template('message', message="Not logged in",
                        logout_link=False,
                        start_link=False)

@route('/login/:token')
def login(token):
    cookie_token = request.get_cookie(TOKEN)
    if cookie_token:
        _, name = get_voter(cookie_token)
        return template('message',
                        message=("Already logged in as %s" % name),
                        logout_link=True,
                        start_link=True)
    else:
        voter = get_voter(token)
        if voter:
            _, name = voter
            response.set_cookie('token', token, path=COOKIE_PATH)
            return template('message',
                             message=("Logged in as %s" % name),
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

def set_db_path(path):
    global db_path
    db_path = path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', default='127.0.0.1',
                        help='The address on which to listen')
    parser.add_argument('-p', '--port', default=8080,
                        help='The port on which to listen')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Run in debug mode')
    parser.add_argument('path', type=str,
                        help='Path to the database file')
    args = parser.parse_args(sys.argv[1:])
    set_db_path(args.path)
    run(host=args.address, port=args.port, debug=args.debug)
