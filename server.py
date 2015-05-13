#!/usr/bin/env python

from bottle import request, response, route, run, static_file

USERS = {
    'abc': 'Bob',
    'def': 'Fred'
}

COOKIE_PATH='/login/'
USERNAME='username'

@route('/login/:token')
def login(token):
    logged_in_user = request.get_cookie(USERNAME)
    if logged_in_user:
        return ("Already logged in as %s" % logged_in_user)
    elif USERS.has_key(token):
        user = USERS[token]
        response.set_cookie('username', user, path=COOKIE_PATH)
        return ("Logged in as %s" % user)
    else:
        return "Invalid token"

@route('/logout')
def logout():
    response.delete_cookie(USERNAME, path=COOKIE_PATH)
    return "Logged out"

@route('/static/<filepath:path>')
def static(filepath):
    return static_file(filepath, root='static/')

run(host='localhost', port=8080, debug=True)
