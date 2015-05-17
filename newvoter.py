#!/usr/bin/env python

import argparse
import os.path
import random
import sqlite3
import string
import sys

def new_voter(path, name):
    token = ''.join(random.choice(string.ascii_uppercase) for i in range(8))
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO voters VALUES(NULL, '%s', '%s')"
                   % (name, token))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str,
                        help='Path to the database file')
    parser.add_argument('name', type=str,
                        help='The name of the new voter')
    args = parser.parse_args(sys.argv[1:])
    if not os.path.exists(args.path):
        raise RuntimeError('Database file does not exist')
    new_voter(args.path, args.name)
