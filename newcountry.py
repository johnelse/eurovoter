#!/usr/bin/env python

"""
Add a new country to the database by name.
"""

import argparse
import os.path
import sqlite3
import sys

def new_country(path, name):
    """
    Add a country with the specified name to the database at the
    specified path.
    """
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO countries VALUES(NULL, '%s')" % name)
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
                        help='The name of the country to add')
    args = parser.parse_args(sys.argv[1:])
    if not os.path.exists(args.path):
        raise RuntimeError('Database file does not exist')
    new_country(args.path, args.name)

if __name__ == "__main__":
    main()
