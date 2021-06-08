"This module implements data import from different file formats."
from __future__ import print_function
from __future__ import absolute_import

__author__ = "Anna Logg (anna@loggsystems.se)"
__date__ = "2008-10-13 -- 2008-12-12"
__copyright__ = "Copyright (C) 2008 Anna Logg"
__license__  = "GNU GPL version 3 or any later version"

from .formats import bibtex, latex, pub
from .validation import validate_papers
from .merging import merge_papers
from publish import config
from .log import print_summary
from .database import read_database, save_database, save_invalid_papers

def import_file(filename, filters=[]):
    "Import data from file into database."

    # Read and validate database
    database_papers = read_database()
    if not config.get("simple_import") :
        (database_papers, invalid_database_papers) = validate_papers(database_papers)
    else :
        invalid_database_papers = []

    # Read imported file
    imported_papers = _read_file(filename)

    # Assign attributes to imported papers
    _assign_attributes(imported_papers, filters)

    # Validate imported file
    if not config.get("simple_import") :
        (imported_papers, invalid_imported_papers) = validate_papers(imported_papers)
    else :
        invalid_imported_papers = []
    print("")
    
    if len(invalid_imported_papers) > 0:
        print('Imported %d paper(s) from "%s" (and found %d invalid paper(s)).' % \
              (len(imported_papers), filename, len(invalid_imported_papers)))
    else:
        print('Imported %d paper(s) from "%s".' % (len(imported_papers), filename))

    # Merge papers
    if config.get("simple_import") :
        merged_papers = database_papers + imported_papers
    else :
        merged_papers = merge_papers(database_papers, imported_papers)

    # Print summary
    print_summary(merged_papers)

    # Save papers to database
    save_database(merged_papers)
    save_invalid_papers(invalid_database_papers + invalid_imported_papers + merged_papers)

def _read_file(filename):
    "Read papers from file"

    # Get the filename suffix
    suffix = filename.split(".")[-1]

    # Choose format based on suffix
    if suffix in ("bib", "bibtex"):
        read = bibtex.read
    elif suffix == "pub":
        read = pub.read
    else:
        raise RuntimeError("Unknown file format.")

    # Open and read file
    try:
        file = open(filename, "r")
        text = file.read()
        file.close()
    except:
        raise RuntimeError('Unable to open file "%s"' % filename)

    # Parse file
    imported_papers = read(text)

    return imported_papers

def _assign_attributes(imported_papers, filters):
    "Assign attributes to imported file"

    for paper in imported_papers:
        for attribute in filters:
            value, should_match = filters[attribute]
            if should_match:
                paper[attribute] = value
            else:
                RuntimeError, "Illegal assignment of attribute: %s!=%s" % (attribute, value)
