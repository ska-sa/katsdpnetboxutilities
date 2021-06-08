"This module implements validation of data from different file formats."
from __future__ import print_function
from builtins import input
from builtins import str
from builtins import range

__author__ = "Anna Logg (anna@loggsystems.se)"
__date__ = "2008-10-27 -- 2008-12-12"
__copyright__ = "Copyright (C) 2008 Anna Logg"
__license__  = "GNU GPL version 3 or any later version"

# Last changed: 2012-08-31
# Modified by Benjamin Kehlet 2012

import os

from publish.common import is_valid, pstr
from publish.formats import pub
from publish.log import warning, print_summary
from publish import config
from publish.algorithms import distance
from publish.interaction import ask_user_yesno, ask_user_alternatives
from publish.database import read_database, save_database, save_invalid_papers
from publish.keygeneration import generate_keys
from publish.merging import process_duplicates

# Maps complete journal name with its issn-number
long2issn = config.get("long2issn")
long2issn = {}

# Maps complete journal name with its abbreviation
long2short = config.get("long2short")
long2short = {}

# Maps journal abbreviation with its complete name
short2long = config.get("short2long")
short2long = {}

def validate_file(filename=None):
    "Validate data in file"

    # Use default database if file is not specified
    if filename is None and not os.path.isfile(config.get("database_filename")):
        print("No file specified and no database found, nothing to do.")
        return

    # Open and read database
    papers = read_database(filename)

    # Validate papers
    (database_papers, invalid_papers) = validate_papers(papers)

    # Generate keys
    database_papers = generate_keys(papers)

    # Check for PDF files
    (num_found, num_missing) = check_pdf_files(papers)

    # Checking for duplicates
    database_papers = process_duplicates(database_papers)

    # Print summary
    print_summary(papers, num_found, num_missing)

    # Save papers to database
    save_database(database_papers)
    save_invalid_papers(invalid_papers)

def validate_papers(papers):
    "Validate list of papers"

    if len(papers) == 0:
        return ([], [])

    print("")
    print("Validating papers")
    print("-----------------")
    print("")

    # Validate each paper in the list of papers
    for paper in papers:
        _validate_paper(paper)

    # Extract valid and invalid papers
    valid_papers   = [paper for paper in papers if is_valid(paper)]
    invalid_papers = [paper for paper in papers if not is_valid(paper)]

    # Print a short summary
    print("")
    print("Validated %d paper(s) ok." % len(valid_papers))
    print("Found %d invalid paper(s)." % len(invalid_papers))
    print("")

    return (valid_papers, invalid_papers)

def _validate_paper(paper):
    "Validate paper, marking it as invalid of not valid"

    print("Validating paper: %s" % pstr(paper))

    # Validate status
    if is_valid(paper):
        _validate_paper_status(paper)

    # Validate that no categories are missing
    if is_valid(paper):
        _validate_paper_categories(paper)

    # Validate all paper strings for typos
    if is_valid(paper):
        _validate_paper_typos(paper)

    # Validate venue
    if is_valid(paper):
        _validate_paper_venue(paper)

    if is_valid(paper) :
        _validate_paper_authors(paper)

    # Validate title
    if is_valid(paper):
        _validate_paper_title(paper)

    # Validate page range
    if is_valid(paper):
        _validate_paper_pages(paper)

def _validate_paper_status(paper):
    "Validate that status is specified"

    # Set status if missing
    if not "status" in paper:
        print('  Status is not defined, assuming status is "published".')
        paper["status"] = "published"

def _validate_paper_categories(paper):
    "Validate that no attributes are missing"

    # Check that category is specified
    if not "category" in paper:
        raise RuntimeError("Unable to validate paper, unknown category.")

    # Check that the paper holds all required attributes
    category = paper["category"]
    category_attributes = config.get("category_attributes")
    for attribute in category_attributes[category]:

        if isinstance(attribute, tuple):
            if not len([a for a in attribute if a in paper]) > 0:
                paper["invalid"] = True
                missing = str(attribute)
                break
        else:
            if not attribute in paper:
                paper["invalid"] = True
                missing = str(attribute)
                break

    if not is_valid(paper):
        print('  Skipping paper (missing attribute "%s")' % missing)
        if not config.get("autofix"):
            input("  Press return to continue.")

def _validate_paper_venue(paper):
    "Validate that the venue (journal, conference etc) is correct"

    # Get venue type
    category = paper["category"]
    category_venues = config.get("category_venues")
    venue_type = category_venues[category] # "journal", "booktitle", etc

    # Skip if venue is None (nothing to check)
    if venue_type is None:
        return

    # Get list of known venues
    known_venues = config.get(venue_type + "s")

    # Check that venue is valid
    venue_name = paper[venue_type]
    if not venue_name in known_venues:
        print("")
        print('  Unknown %s: "%s"' % (venue_type, venue_name))
        suggested_venue = _suggest_venue(venue_name, known_venues)
        if suggested_venue is None:
            if ask_user_yesno('  Would you like to add %s "%s"?' % (venue_type, venue_name), "no"):
                _add_venue(venue_type, venue_name)
            else:
                print("  Skipping paper.")
                paper["invalid"] = True
        else:
            print('  Suggested %s: "%s"' % (venue_type, suggested_venue))
            alternative = ask_user_alternatives("  Unknown %s, what should I do?" % venue_type,
                                                ("Replace %s." % venue_type,
                                                 "Add %s." % venue_type,
                                                 "Skip paper."))
            print("")
            if alternative == 0:
                paper[venue_type] = suggested_venue
            elif alternative == 1:
                _add_venue(venue_type, venue_name)
            elif alternative == 2:
                print("  Skipping paper (unable to guess the right %s)" % venue_type)
                input("  Press return to continue.")
                paper["invalid"] = True
            else:
                raise RuntimeError("Unknown option.")

def _validate_paper_authors(paper) :
    "Validate spelling of the author names"

    allowed_author_names = config.get("allowed_author_names")

    # Skip if there is nothing to check
    if allowed_author_names is None:
        return

    for i, author in enumerate(paper["author"]) :
        if not author in allowed_author_names :
            print("\n  Unknown author: \"%s\"" % author)
            suggested_author = _suggest_venue(author, allowed_author_names)
            if suggested_author is None:
                if ask_user_yesno('  Would you like to add %s"?' % (author), "no"):
                    _add_author(author)
                else:
                    print("  Skipping paper.")
                    paper["invalid"] = True
            else:
                print('  Suggested "%s"' % (suggested_author))
                alternative = ask_user_alternatives("  Unknown author, what should I do?",
                                                    ("Replace author.",
                                                     "Add author.",
                                                     "Skip paper."))
                print("")
                if alternative == 0:
                    paper["author"][i] = suggested_author
                elif alternative == 1:
                    _add_author(suggested_author)
                elif alternative == 2:
                    print("  Skipping paper (unable to guess the right author)")
                    input("  Press return to continue.")
                    paper["invalid"] = True
                else:
                    raise RuntimeError("Unknown option.")



def _validate_paper_title(paper):
    "Validate that the title is correct, fix capitalization"

    # Fix capitalization
    title = paper["title"]
    for separator in (" ", "-"):

        words = title.split(separator)

        lowercase = config.get("lowercase")
        uppercase = config.get("uppercase")
        new_words = []
        for i in range(len(words)):
            word = words[i]
            if word == "":
                continue
            if word.lower() in lowercase:
                word = word.lower()
            elif word.lower() in uppercase:
                word = uppercase[word.lower()]
            else:
                word = word[0].upper() + word[1:]
            new_words.append(word)

        title = separator.join(new_words)

    paper["title"] = title

def _validate_paper_pages(paper):
    "Validate page range"

    # Only check if we have pages
    if not "pages" in paper:
        return
    pages = paper["pages"]

    invalid = False
    new_pages = pages

    # Check if page page must contain "-"
    if config.get("require_page_range") and not "-" in pages:
        invalid = True
    if "-" in pages:
        if "--" in pages:
            first, last = pages.split("--")[:2]
        else:
            first, last = pages.split("-")[:2]
            if len(first) == 0 or len(last) == 0:
                invalid = True

            # Reformat string
            new_pages = first.strip() + config.get("page_separator") + last.strip()

    # Check for invalid page string
    if invalid:
        paper["invalid"] = True
        print("  Incorrectly formatted page string: " + pages)
        if not config.get("autofix"):
            input("  Skipping paper, press return to continue.")
        else:
            print("  Skipping paper.")
        return


    # Check if string was changed
    if not new_pages == pages:
        print("  Incorrectly formatted page string: " + pages)
        print("  Suggested correction:              " + new_pages)
        if ask_user_yesno("  Would you like to accept the suggested correction:"):
            print("  Correcting page string.")
            paper["pages"] = new_pages
        else:
            paper["invalid"] = True
            if not config.get("autofix"):
                input("  Skipping paper, press return to continue.")
            else:
                print("  Skipping paper.")

def _validate_paper_typos(paper):
    "Validate all paper strings for typos"

    typos = config.get("typos")

    # Check all attributes
    for attribute in paper:

        # Extract typos to check
        attribute_typos = typos["common"].copy()
        if attribute in typos:
            for typo in typos[attribute]:
                attribute_typos[typo] = typos[attribute][typo]

        # Get attribute value and convert to tuple
        value = paper[attribute]
        if isinstance(value, tuple):
            value_tuple = value
        else:
            value_tuple = (value,)

        # Check all values in tuple
        new_values = []
        for value in value_tuple:
            for typo in attribute_typos:
                replacement = attribute_typos[typo]

                # Check for typo
                if typo in value:
                    print("  Incorrectly formatted %s string: %s" % (attribute, str(value)))

                    if replacement is None:

                        # Found no replacement, skip paper
                        paper["invalid"] = True
                        if config.get("autofix"):
                            print("  Skipping paper")
                        else:
                            input("  Skipping paper, press return to continue.")
                        return

                    else:

                        # Found replacement
                        value = value.replace(typo, replacement)
                        print('  Replacing typo "%s" with "%s".' % (typo, replacement))
                        if not config.get("autofix"):
                            print("  Press return to continue.")

            new_values.append(value)

        # Assign corrected value
        if isinstance(paper[attribute], tuple):
            paper[attribute] = tuple(new_values)
        else:
            paper[attribute] = new_values[0]

def _suggest_venue(venue, known_venues):
    "Suggest venue name"

    matching_distance = config.get("matching_distance_weak")
    suggested_venue = None
    min_distance = 1.0

    # Look for closes match
    for v in known_venues:
        d = distance(venue.lower(), v.lower())
        if d < matching_distance and d < min_distance:
            suggested_venue = v
            min_distance = d

    # If not found try matching substrings
    if suggested_venue is None:
        for v in known_venues:
            d = distance(venue.lower(), v.lower())
            if venue in v or v in venue and d < min_distance:
                suggested_venue = v

    return suggested_venue

def _add_venue(venue_type, venue_name):
    "Add venue to known venues"

    # Append to list of known venues (remember at run-time)
    known_venues = config.get(venue_type + "s")
    known_venues.append(venue_name)

    # Append to file
    filename = config.get("local_venues_filename")
    try:
        file = open(filename, "a")
        file.write("%s: %s\n" % (venue_type, venue_name))
    except:
        raise RuntimeError('Unable to add local venue to file "%s".' % filename)

def _add_author(author_name) :
    allowed_author_names = config.get("allowed_author_names")
    allowed_author_names.add(author_name)

    # Append to file
    filename = config.get("authornames_filename")

    try:
        file = open(filename, "a")
        file.write(author_name.strip()+"\n")
    except:
        raise RuntimeError('Unable to author to file: "%s".' % filename)


def check_pdf_files(papers):
    "Check which PDF files are missing (if any)"

    print("Checking for PDF files")
    print("----------------------")
    print("")

    # Iterate over papers
    num_found = 0
    num_missing = 0
    for paper in papers:

        # Skip some categories
        if paper["category"] in ["courses"]:
            continue

        # Generate name of PDF file
        pdffile = os.path.join("papers", paper["key"] + ".pdf")
        if os.path.isfile(pdffile):
            num_found += 1
            paper["pdf"] = pdffile
        else:
            print("Missing PDF file %s for paper: %s" % (pdffile, pstr(paper)))
            num_missing += 1
            paper["pdf"] = "missing"

    return (num_found, num_missing)
