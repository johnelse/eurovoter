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


def save_votes(voter_id, post):
    """
    Save a user's set of votes in the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("DELETE FROM votes WHERE voter_id = %d" % voter_id)
    for score in SCORES:
        key = "%dpoints" % score
        country_id = post.get(key)
        if not country_id == 'None':
            cursor.execute("INSERT INTO votes VALUES(%d, %d, %d)"
                           % (voter_id, int(country_id), score))
    conn.commit()
    conn.close()


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


@route('/results')
def results():
    """
    Serve the results page.
    """
    results_list = []
    countries = get_countries()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for country_id, country_name in countries:
        cursor.execute("SELECT * FROM VOTES WHERE country_id = %d"
                       % country_id)
        total_score = 0
        for row in cursor:
            total_score += row[2]
        results_list.append((country_name, total_score))
    conn.close()

    results_list_sorted = sorted(results_list,
                                 key=(lambda x: x[1]),
                                 reverse=True)

    return template('results', results=results_list_sorted)


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
    cookie_token = request.get_cookie(TOKEN)
    if cookie_token:
        try:
            voter_id, _ = get_voter(cookie_token)
            save_votes(voter_id, request.POST)
            return "Ok"
        except RuntimeError:
            return "An error occurred"
    else:
        return "Not logged in"


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
