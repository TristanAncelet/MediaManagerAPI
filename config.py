#!/usr/bin/python3

import os 
import sys

import logging
import sqlite3

logging.basicConfig(level = logging.DEBUG)

# This is the commandline configuration tool for my service

connection = sqlite3.connect("files/database.db")

def append_directory_to_list(directory):
    c = connection.cursor()
    """-a : Append Directory to managed Directories"""
    c.execute("INSERT INTO managed_locations(name, location) values(?, ?)",(os.path.basename(directory), directory, ))
    c.close()
    connection.commit()

def list_managed_directories():
    c = connection.cursor()
    locations = [location[0] for location in list(c.execute("SELECT location FROM managed_locations").fetchall())]
    print("\n".join(locations))

            


if __name__ == "__main__":
    args = sys.argv[1:]
    
    flags = list()

    for item in args:
        if '-' in item:
            flags.append(item)

    if '-a' in flags:
        append_directory_to_list(args[-1])
    
    if '-l' in flags:
        list_managed_directories()



