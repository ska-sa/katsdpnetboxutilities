"""This module provides functionality for reading and writing papers
from the database."""
from __future__ import print_function
from __future__ import absolute_import

__author__ = "Anna Logg (anna@loggsystems.se)"
__date__ = "2008-12-12 -- 2008-12-12"
__copyright__ = "Copyright (C) 2008 Anna Logg"
__license__  = "GNU GPL version 3 or any later version"

import shutil
import os.path
import time

from .formats import pub
from publish import config
from .common import is_valid

def read_database(database_filename=None):
    "Read papers from database"

    # Get location of database file
    if database_filename is None:
        database_filename = config.get("database_filename")

    # Open and read database
    try:
        file = open(database_filename, "r")
        text = file.read()
        file.close()
    except Exception as e:
        return []

    # Parse file
    database_papers = pub.read(text)

    return database_papers

def save_database(merged_papers):
    "Save to database and make a backup copy if needed"

    database_filename = config.get("database_filename")

    # Generate text to be written to file
    text = pub.write(merged_papers)

    print("")

    # Make backup copy if needed (file size of generated file is different from the current)
    # TODO: Register if changes has been made and write backup file based on that
    #       (instead of just comparing file sizes)
    if os.path.isfile(database_filename) and len(text) != os.path.getsize(database_filename):
        backup_filename = database_filename + ".bak"
        print('Saving backup copy of database to file "%s"' % backup_filename)
        try:
            shutil.copyfile(database_filename, backup_filename)
        except:
            raise RuntimeError("Unable to create backup copy of database")

    # Open and read file
    print('Saving database to file "%s"' % database_filename)
    try:
        file = open(database_filename, "w")
        file.write(text)
    except UnicodeEncodeError as e:
        try:
            file.write(text.encode('utf-8'))
        except Exception as e:
            raise RuntimeError('Unable to save database to file "%s"\n%s' % (database_filename, str(e)))

    file.close()

def save_invalid_papers(papers):
    "Save invalid papers to file"

    # Extract invalid papers
    invalid_papers = []
    for paper in papers:
        if not is_valid(paper):
            invalid_papers.append(paper)

    # Don't save if there are no invalid papers
    if len(invalid_papers) == 0:
        return

    # Generate filename
    date = time.strftime("%Y%m%d-%H:%m:%S")
    invalid_filename = config.get("invalid_filename_prefix") + "-" + date + ".pub"

    # Write to file
    text = pub.write(invalid_papers)
    print('Saving invalid papers to "%s".' % invalid_filename)
    try:
        file = open(invalid_filename, "w")
        file.write(text)
        file.close()
    except:
        raise RuntimeError('Unable to save invalid papers to file "%s"' % invalid_filename)
