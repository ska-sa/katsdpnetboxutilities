
"This module handles writing of log messages etc."
from __future__ import print_function
from builtins import str

__author__ = "Anna Logg (anna@loggsystems.se)"
__date__ = "2008-10-27 -- 2008-11-08"
__copyright__ = "Copyright (C) 2008 Anna Logg"
__license__  = "GNU GPL version 3 or any later version"

from sys import exit
from publish import config

def warning(message):
    "Print a warning"
    print("*** Warning: " + str(message))

def info(message):
    "Print an information message"
    print(str(message))

def error(message):
    "Print an error message"
    print("*** Error: " + str(message))

def print_summary(papers, num_found=0, num_missing=0):
    "Print summerazed result"

    print("")
    print("Summary of papers")
    print("-----------------")
    print("")

    if not (num_found == 0 and num_missing == 0):
        print("Database has %d paper(s)." % len(papers))
        print("PDF files found for %d paper(s), %d missing." % (num_found, num_missing))
        print("")

    headings = config.get("category_headings")
    categories = config.get("categories")

    # Make correct indentation for each attribute-value pair
    max_heading = max([len(headings[category]) for category in categories])

    # Count number of papers in each category
    for category in categories:
        num_papers = len([paper for paper in papers if paper["category"] == category])
        heading = headings[category]
        indentation = " " * (max_heading - len(heading))
        print("%s: %s%d" % (heading, indentation, num_papers))
    print("%s: %s%d" % ("Total", " " * (max_heading - len("Total")), len(papers)))
