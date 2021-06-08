"This module implements input/output for pub."
from builtins import str

__author__ = "Anna Logg (anna@loggsystems.se)"
__date__ = "2008-10-22 -- 2008-11-11"
__copyright__ = "Copyright (C) 2008 Anna Logg"
__license__  = "GNU GPL version 3 or any later version"

# Modified by Anders Logg 2012
# Modified by Benjamin Kehlet 2012
# Last changed: 2012-08-31

import re, sys

from publish.common import is_valid, ordered_attributes
from publish import config

# Pattern used for extracting the pub-categories
_category_list = "|".join([category for category in config.get("category_attributes")])
_category_pattern =  re.compile('^\*\s*(%s)\s*$' % _category_list, re.IGNORECASE)

# Pattern used for extracting title
_title_pattern = re.compile('^\*\*\s*(.*?)\s*$')

# Attributes to ignore
_ignores = ["invalid"]

def read(text):
    "Extract papers from text and return papers as a list of dictionaries."

    papers = []
    paper = None
    category = None
    title = None
    lines = text.split("\n")
    for line in lines:
        if sys.version[0] == '2':
            try:
                str(line)
            except UnicodeDecodeError as e:
                line = line.decode('utf-8')

        line = line.strip()

        # Look for start of category
        #match = _category_pattern.search(line)
        if line.startswith("* ") :

            # Extract category
            #groups = match.groups()
            #category = groups[0]
            category = line[2:]

            # Make sure every category is written in lower-case letters
            category = category.lower()

            continue

        # Look for start of paper
        match = _title_pattern.search(line)
        if not match is None:

            # Check that the category has been specified
            if category is None:
                raise RuntimeError("Found paper but category has not been specified.")

            # Extract title
            groups = match.groups()
            title = groups[0]

            # Save current paper if any
            if not paper is None:

                if "author" in paper:
                    paper["author"] = _extract_authors(paper, "author")
                if "editor" in paper:
                    paper["editor"] = _extract_authors(paper, "editor")

                if "allowed_duplicates" in paper :
                    # Split wrt whitespaces
                    paper["allowed_duplicates"] = paper['allowed_duplicates'].split()

                papers.append(paper)

            # Reset paper
            paper = {"title": title, "category": category}

            continue

        # Look for attribute
        if ":" in line:

            # Check that the title has been specified
            if title is None:
                raise RuntimeError("Found attribute but title has not been specified.")

            # Extract attribute and value
            attribute = line.split(":")[0].strip()
            value = ":".join(line.split(":")[1:]).strip()

            # Add attribute-value pair to paper
            if not attribute in _ignores:
                paper[attribute] = value

    # Save last paper if any
    if not paper is None:

        if "author" in paper:
            paper["author"] = _extract_authors(paper, "author")
        if "editor" in paper:
            paper["editor"] = _extract_authors(paper, "editor")

        papers.append(paper)

    return papers

def write(papers):
    "Format the given list of papers in the pub format."

    text = []

    if config.get("use_standard_categories") :
        categories = config.get("categories")
    else :
        categories = set()
        for paper in papers :
            categories.add(paper["category"])
        categories = list(categories)
        categories.sort()


    # Iterate over categories
    for category in categories:

        # Extract papers in category
        category_papers = [paper for paper in papers
                           if paper["category"] == category]
        if len(category_papers) == 0:
            continue

        # Write category
        text.append("* %s\n" % category)

        # Iterate over papers in category
        for paper in category_papers:

            # Write title
            if "title" in paper:
                title = paper["title"]
            else:
                title = "missing"
            try:
                text.append("** %s\n" % title)
            except UnicodeDecodeError as e:
                text.append("** %s\n" % title.decode('utf-8'))

            # Write attributes
            text.append(write_paper(paper, ["category", "title"] + _ignores))

    return "".join(text)

def write_paper(paper, ignores=[]):
    "Format given paper in the pub format"

    text = []

    # Extract which attributes to write (first required, then others)
    attributes = ordered_attributes(paper, ignores)

    # Make correct indentation for each attribute-value pair
    max_attr = max([len(attribute) for attribute in attributes])

    # Write attribute-value pairs
    for attribute in attributes:
        # Compute indendation
        indentation = " " * (max_attr - len(attribute))

        # Make sure we may write invalid papers with missing attributes
        if not attribute in paper:
            value = "missing"
        elif attribute == "author":
            value = ", ".join(paper["author"])
        elif attribute == "editor":
            value = ", ".join(paper["editor"])
        elif attribute == "allowed_duplicates" :
            value = " ".join(paper["allowed_duplicates"])
        else:
            value = paper[attribute]

        # Write attribute-value pair
        text.append("   %s: %s%s\n" % (attribute, indentation, value))

    return "".join(text)

def write_diff(paper0, paper1):
    "Write readable diff between papers"

    text = ""

    # Generate text for papers
    s0 = write_paper(paper0)
    s1 = write_paper(paper1)

    text += "First paper:\n\n"

    # Mark differences for first paper
    for line in s0.split("\n"):
        if not ":" in line: continue
        attribute = line.split(":")[0].strip()
        if attribute in paper1 and paper0[attribute] == paper1[attribute]:
            text += "    " + line.strip() + "\n"
        else:
            text += "--> " + line.strip() + "\n"

    text += "\nSecond paper:\n\n"

    # Mark differences for second paper
    for line in s1.split("\n"):
        if not ":" in line: continue
        attribute = line.split(":")[0].strip()
        if attribute in paper0 and paper0[attribute] == paper1[attribute]:
            text += "    " + line.strip() + "\n"
        else:
            text += "--> " + line.strip() + "\n"

    return text

def _extract_authors(paper, attribute):
    "Extract authors as tuple from string"

    author = paper[attribute]
    names = author.split(",")

    authors = []
    for name in names:
        name = name.strip()

        # Add missing . for initials and cleanup spaces
        words = name.split(" ")
        new_words = []
        for word in words:
            word = word.strip()
            if len(word) == 1:
                new_words.append(word + ".")
            elif len(word) > 1:
                new_words.append(word)
        name = " ".join(new_words)

        authors.append(name)

    return authors
