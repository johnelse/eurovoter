#!/usr/bin/env python

from bottle import request, response, route, run, static_file, template

USERS = {
    'abc': 'Bob',
    'def': 'Fred'
}

COOKIE_PATH='/'
USERNAME='username'

@route('/')
def home():
    logged_in_user = request.get_cookie(USERNAME)
    if logged_in_user:
        return template('main', name=logged_in_user)
    else:
        return template('message', message="Not logged in",
                        logout_link=False,
                        start_link=False)

@route('/login/:token')
def login(token):
    logged_in_user = request.get_cookie(USERNAME)
    if logged_in_user:
        return template('message',
                        message=("Already logged in as %s" % logged_in_user),
                        logout_link=True,
                        start_link=True)
    elif USERS.has_key(token):
        user = USERS[token]
        response.set_cookie('username', user, path=COOKIE_PATH)
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
    response.delete_cookie(USERNAME, path=COOKIE_PATH)
    return template('message',
                    message="Logged out",
                    logout_link=False,
                    start_link=False)

@route('/static/<filepath:path>')
def static(filepath):
    return static_file(filepath, root='static/')

run(host='localhost', port=8080, debug=True)
