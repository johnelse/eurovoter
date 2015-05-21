#!/usr/bin/env python

"""
Create a new empty database with the correct schema.
"""

import argparse
import os.path
import sqlite3
import sys


def create_db(path):
    """
    Create a database at the specified path.
    """
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE voters(
                       id INTEGER PRIMARY KEY,
                       name TEXT UNIQUE,
                       token TEXT UNIQUE)
                   ''')
    cursor.execute('''CREATE TABLE countries(
                       id INTEGER PRIMARY KEY,
                       name TEXT UNIQUE)
                   ''')
    cursor.execute('''CREATE TABLE votes(
                       voter_id INTEGER,
                       country_id INTEGER,
                       points INTEGER,
                       FOREIGN KEY(voter_id) REFERENCES voters(id),
                       FOREIGN KEY(country_id) REFERENCES countries(id))
                   ''')
    conn.commit()
    conn.close()


def main():
    """
    Program entry point.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str,
                        help='Path at which the database should be created')
    args = parser.parse_args(sys.argv[1:])
    if os.path.exists(args.path):
        raise RuntimeError('File already exists')
    create_db(args.path)


if __name__ == "__main__":
    main()
