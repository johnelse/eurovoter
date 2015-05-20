#!/usr/bin/env python


"""
Add a new voter to the database, and generate a login token.
"""

import argparse
import os.path
import random
import sqlite3
import string
import sys


def new_voter(path, name):
    """
    Add a voter with the specified name to the database at the
    specified path, along with a randomly-generated login token.
    """
    token = ''.join(random.choice(string.ascii_uppercase) for i in range(8))
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO voters VALUES(NULL, '%s', '%s')"
                   % (name, token))
    conn.commit()
    conn.close()


def main():
    """
    Program entry point.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str,
                        help='Path to the database file')
    parser.add_argument('name', type=str,
                        help='The name of the new voter')
    args = parser.parse_args(sys.argv[1:])
    if not os.path.exists(args.path):
        raise RuntimeError('Database file does not exist')
    new_voter(args.path, args.name)


if __name__ == "__main__":
    main()
