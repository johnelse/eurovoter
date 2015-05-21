#!/usr/bin/env python


"""
Main web application implementation.
"""

import argparse
from bottle import request, response, route, run, static_file, template
import sqlite3
import sys

COOKIE_PATH = '/'
TOKEN = 'token'

SCORES = [12, 10, 8, 7, 6, 5, 4, 3, 2, 1]

DB_PATH = ""


def get_countries():
    """
    Get an alphabetised list of countries from the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM countries ORDER BY name")
    result = cursor.fetchall()
    conn.close()
    return result


def get_voter(token):
    """
    Get the voter corresponding to the supplied token.
    """
    conn = sqlite3.connect(DB_PATH)
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
    """
    Serve the main voting page.
    """
    cookie_token = request.get_cookie(TOKEN)
    if cookie_token:
        _, name = get_voter(cookie_token)
        countries = get_countries()
        return template('main', name=name, countries=countries, scores=SCORES)
    else:
        return template('message', message="Not logged in",
                        logout_link=False,
                        start_link=False)


@route('/login/:token')
def login(token):
    """
    Login the user with the specified token.
    """
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
    """
    Logout of the system.
    """
    response.delete_cookie(TOKEN, path=COOKIE_PATH)
    return template('message',
                    message="Logged out",
                    logout_link=False,
                    start_link=False)


@route('/static/<filepath:path>')
def static(filepath):
    """
    Serve a static file at the requested path.
    """
    return static_file(filepath, root='static/')


@route('/formsubmit', method='POST')
def formsubmit():
    """
    Receive a form submission.
    """
    return "Ok"


def set_db_path(path):
    """
    Set the global database path.
    """
    global DB_PATH
    DB_PATH = path


def main():
    """
    Program entry point.
    """
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


if __name__ == "__main__":
    main()
