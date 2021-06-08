"This module implements data export to different file formats."
from __future__ import print_function
from __future__ import absolute_import

__author__ = "Anders Logg (logg@simula.no)"
__date__ = "2010-01-04 -- 2010-01-04"
__copyright__ = "Copyright (C) 2010 Anders Logg"
__license__  = "GNU GPL version 3 or any later version"

from publish.importing import read_database
from .validation import validate_papers
from .filtering import filter_papers
from .log import print_summary
from publish import config

def print_file(filters=[]):
    "Print data to stdout"

    # Read database
    database_filename = config.get("database_filename")
    database_papers = read_database(database_filename)

    # Validate papers
    #(valid_papers, invalid_papers) = validate_papers(database_papers)
    valid_papers = database_papers

    # Filter papers
    filtered_papers = filter_papers(valid_papers, filters)

    # Print papers
    print()
    for paper in filtered_papers:
        _print_paper(paper)
        print()

    # Print summary
    print_summary(filtered_papers)

def _print_paper(paper):
    "Print paper"
    print(paper["title"])
    print("-"*len(paper["title"]))
    paper_copy = paper.copy()
    del paper_copy["title"]
    _print_table(paper)

def _print_table(dictionary):
    "Print dictionary as a two-column table"
    colsize = max(len(key) for key in dictionary)
    for (key, value) in dictionary.items():
        print("%s:%s%s" % (key, (colsize - len(key) + 1)*" ", value))
