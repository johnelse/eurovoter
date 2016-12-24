#!/usr/bin/env python


"""
Main web application implementation.
"""

import argparse
import sys
from bottle import install
from bottle import request, response, route, run, static_file, template
from bottle_sqlite import SQLitePlugin

COOKIE_PATH = '/'
TOKEN = 'token'

SCORES = [12, 10, 8, 7, 6, 5, 4, 3, 2, 1]


def get_countries(db):
    """
    Get an alphabetised list of countries from the database.
    """
    cursor = db.cursor()
    cursor.execute("SELECT * FROM countries ORDER BY name")
    result = cursor.fetchall()
    return result


def get_voter(db, token):
    """
    Get the voter corresponding to the supplied token.
    """
    cursor = db.cursor()
    cursor.execute("SELECT * FROM voters WHERE token = '%s'" % token)
    result = cursor.fetchone()
    if result:
        voter_id, name, _ = result
        return (voter_id, name)
    else:
        return None


def get_previous_votes(db, voter_id):
    """
    Get a dictionary of a voter's previous votes. Keys are the scores, values
    are the country IDs.
    """
    votes = {}
    cursor = db.cursor()
    cursor.execute("SELECT * FROM votes WHERE voter_id = %d" % voter_id)
    for row in cursor:
        votes[row[2]] = row[1]
    return votes


def save_votes(db, voter_id, post):
    """
    Save a user's set of votes in the database.
    """
    cursor = db.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("DELETE FROM votes WHERE voter_id = %d" % voter_id)
    for score in SCORES:
        key = "%dpoints" % score
        country_id = post.get(key)
        if country_id != 'None':
            cursor.execute("INSERT INTO votes VALUES(%d, %d, %d)"
                           % (voter_id, int(country_id), score))
    db.commit()


@route('/')
def home(db):
    """
    Serve the main voting page.
    """
    cookie_token = request.get_cookie(TOKEN)
    if cookie_token:
        voter_id, name = get_voter(db, cookie_token)
        countries = get_countries(db)
        previous_votes = get_previous_votes(db, voter_id)
        return template('main', name=name,
                        countries=countries,
                        previous_votes=previous_votes,
                        scores=SCORES)
    else:
        return template('message', message="Not logged in",
                        logout_link=False,
                        start_link=False)


@route('/results')
def results(db):
    """
    Serve the results page.
    """
    results_list = []
    countries = get_countries(db)
    cursor = db.cursor()
    for country_id, country_name in countries:
        cursor.execute("SELECT * FROM VOTES WHERE country_id = %d"
                       % country_id)
        total_score = 0
        for row in cursor:
            total_score += row[2]
        results_list.append((country_name, total_score))

    results_list_sorted = sorted(results_list,
                                 key=(lambda x: x[1]),
                                 reverse=True)

    return template('results', results=results_list_sorted)


@route('/login/:token')
def login(db, token):
    """
    Login the user with the specified token.
    """
    cookie_token = request.get_cookie(TOKEN)
    if cookie_token:
        _, name = get_voter(db, cookie_token)
        return template('message',
                        message=("Already logged in as %s" % name),
                        logout_link=True,
                        start_link=True)
    else:
        voter = get_voter(db, token)
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
def formsubmit(db):
    """
    Receive a form submission.
    """
    cookie_token = request.get_cookie(TOKEN)
    if cookie_token:
        try:
            voter_id, _ = get_voter(db, cookie_token)
            save_votes(db, voter_id, request.POST)
            return "Ok"
        except RuntimeError:
            return "An error occurred"
    else:
        return "Not logged in"


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
    install(SQLitePlugin(dbfile=args.path))
    run(host=args.address, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
