#!/usr/bin/env python

import argparse
import os.path
import random
import sqlite3
import string
import sys

def new_country(path, name):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO countries VALUES(NULL, '%s')" % name)
    conn.commit()
    conn.close()

def main():
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
