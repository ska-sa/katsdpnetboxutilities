"This module handles filtering of papers based on attributes."
from __future__ import absolute_import

__author__ = "Anna Logg (anna@loggsystems.se)"
__date__ = "2008-11-11 -- 2009-08-30"
__copyright__ = "Copyright (C) 2008-2009 Anna Logg"
__license__  = "GNU GPL version 3 or any later version"

from .common import short_author

def filter_papers(papers, filters):
    "Filters papers, for instance it enables to get papers from a specific year"

    filtered_papers = []
    for paper in papers:
        match = True
        for attribute in filters:
            value, should_match = filters[attribute]
            if attribute == "author" or attribute == "editor":
                if not matching_author(paper[attribute], value, should_match):
                    match = False
                    break
            else:
                for val in value.split(","):
                    if not matching_attribute(paper, attribute, val, should_match):
                        match = False
                        break
        if match:

            # Remove private key
            paper = paper.copy()
            if "private" in paper:
                del paper["private"]

            # Append paper
            filtered_papers.append(paper)

    return filtered_papers

def matching_attribute(paper, attribute, value, should_match):
    "Check if attribute matches"

    # Check for match
    match = attribute in paper and paper[attribute] == value

    # Should either match or not
    if should_match:
        return match
    else:
        return not match

def matching_author(authors, value, should_match):
    "Check if author matches"

    # Match is case-insensitive
    value = value.lower()

    # Check for match
    match = False
    for author in authors:

        # Check match against full name and abbreviation
        author_lower = author.lower()
        author_short = short_author(author).lower()
        if value in author_lower or value in author_short:
            match = True
            break

    # Should either match or not
    if should_match:
        return match
    else:
        return not match
