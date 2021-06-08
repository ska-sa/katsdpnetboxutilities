"This module implements input/output for BibTeX."
from __future__ import print_function
from builtins import str
from builtins import input
from builtins import range

__author__    = "Anna Logg (anna@loggsystems.se)"
__date__      = "2008-10-05 -- 2008-11-11"
__copyright__ = "Copyright (C) 2008 Anna Logg"
__license__   = "GNU GPL version 3 or any later version"

# Modified by Benjamin Kehlet 2011
# Modified by Anders Logg 2012
# Last changed: 2012-01-30

import re

from publish.common import pstr, ordered_attributes
from publish import config
from publish.exceptions import ParseException

# Pattern used for extracting the BibTeX-fields
_entry_list = "|".join([entry_type for entry_type in config.get("entrytype_attributes")])
_entry_pattern = re.compile('^(%s)\s*{' % _entry_list, re.IGNORECASE)

# Pattern used for extracting everything before and after the "="-sign
#_block_pattern = re.compile('\s*(.*?)\s*=\s*{(.*?)}\s*,')

# Pattern used for extracting attribute
_attribute_pattern = re.compile('\s*,*(.*?)\s*=\s*')

# Attributes to ignore
_ignores = ["invalid", "pdf", "status", "category"]

def read(text):
    text = text.strip()
    "Extract papers from text and return papers as a list of dictionaries."

    print("")
    print("Importing papers from BibTeX")
    print("----------------------------")
    print("")

    papers = []
    position = 0

    while position < len(text) :
        current_paper = {}

        position = _skip_spaces(position, text)

        # Look for '@' at start of paper
        if not text[position] == "@" :
            raise ParseException("BibTeX parse error expected '@' near '%s'" % _get_line(position, text))

        position += 1

        # Extract entry-type
        entrytype_orig = text[position:position+text[position:].find("{")].strip()
        entrytype = entrytype_orig.lower()  # bring everything to lower case
        #match = re.search(_entry_pattern, text[position:])  # old

        if config.get("use_standard_categories") and entrytype not in config.get("entrytype_attributes") :
            #if not match :
            msg  = "Parse error in BibTeX file\n%s\n" % _get_line(position, text)
            msg += 'Found entry "%s"; allowed entry types are: %s' % (entrytype_orig, ", ".join(config.get("entrytype_attributes")))
            raise ParseException(msg)

        # Make sure every entry-type is written in lower-case letters
        #current_paper["entrytype"] = match.group(1).lower()
        current_paper["entrytype"] = entrytype

        position += len(current_paper["entrytype"])
        position = _skip_spaces(position, text)

        if not text[position] == "{" :
            raise ParseException("Bibtex parse error. Expected '{' after entrytype. Got '%s'\n%s" % (text[position], _get_line(position, text)))

        position += 1

        # Find the ',' which separates the key from the attributes
        index = text[position:].find(",")

        current_paper["key"] = text[position:position+index].strip()

        # skip through the key and the following ','
        position += index+1
        position = _skip_spaces(position, text)

        # collect all the attributes
        while True :
            position, attr_key, attr_value = _parse_attribute(position, text)
            position = _skip_spaces(position, text)

            # Bibtex attribute "key" is legal and needed for sorting if
            # author is missing (typical in software entries). Let
            # Bibtex "key" correspond to "sortkey" in publish
            if attr_key == "key":
                attr_key = "sortkey"

            if attr_key in current_paper :
                raise ParseException("Paper with key '%s' has double declared attribute: '%s'" % (current_paper["key"], attr_key))

            current_paper[attr_key] = attr_value

            if text[position] != "," and text[position] != "}" :
                raise ParseException("Unexpected character '%s' at %s" % (text[position], _get_line(position, text)))

            position = _skip_spaces(position ,text)
            if text[position] == "," :
                position += 1
                position = _skip_spaces(position, text)

            # Note that a comma is allowed after the last attribute
            if text[position] == "}" :
                break


        position += 1
        position = _skip_spaces(position, text)

        # Done with parsing the paper. Now validate the collected data

        # Check that paper has all required attributes
        if config.get("use_standard_categories") :
            _check_paper(current_paper)
        else :
            if "status" not in current_paper :
                current_paper["status"] = "published"

        # Extract category
        if config.get("use_standard_categories") :
            current_paper["category"] = _extract_category(current_paper)
        else :
            current_paper["category"] = current_paper["entrytype"]

        # Extract authors as tuple from string
        if "author" in current_paper:
            _extract_authors(current_paper, "author")

        # Extract editors as tuple from string
        if "editor" in current_paper:
            _extract_authors(current_paper, "editor")

        papers.append(current_paper)

    # Return list of papers
    return papers

def _parse_attribute(position, text) :
    eq_pos = text[position:].find("=")

    if eq_pos < 1 :
      raise ParseException("Bibtex parse error, expected attribute=value near '%s'" % _get_line(position, text))

    key = text[position:position+eq_pos].strip()

    position += eq_pos+1

    position, value = _parse_attribute_value(position, text)
    return (position, key, value)

def _parse_attribute_value(position, text) :
    position = _skip_spaces(position, text)

    if not text[position] == "{" :
        raise ParseException("Expected '{' near '%s'" % _get_line(position, text))

    position += 1

    # Look for the end point, by counting the braces
    num_left_braces = 1
    num_right_braces= 0
    end_pos = position
    for end in range(position, len(text)):

        # Count braces
        if text[end] == "{" and not text[end - 1] == "\\" :
            num_left_braces += 1
        elif text[end] == "}" and not text[end -1] == "\\" :
            num_right_braces += 1

        # Found end of paper, done
        if num_left_braces == num_right_braces:
            break

    #orig: return (end+1, text[position:end].strip())
    value = text[position:end].strip().replace('\n', ' ')
    value = re.sub(r' +', ' ', value)
    return (end+1, value)


def write(papers):
    "Format the given list of papers in the BibTeX format."

    text = ""

    for (i, paper) in enumerate(papers):
        entry_type = config.get("category2entrytype")[paper["category"]]
        if "key" in paper:
            key = paper["key"]
        else:
            key = "paper%d" % i
        text += "@%s{%s,\n" % (entry_type, key)
        for attribute in ordered_attributes(paper, _ignores):
            if attribute in ("entrytype", "key"):
                continue
            if attribute == "sortkey":
                attribute = "key"  # sortkey becomes key in Bibtex
            if attribute == "author":
                value = " and ".join(paper["author"])
            elif attribute == "editor":
                value = " and ".join(paper["editor"])
            else:
                value = str(paper[attribute])
            text += "  %s = {%s},\n" % (attribute, value)
        text += "}\n"
        if not paper == papers[-1]:
            text += "\n"

    return text

def _parse_paper(block, value_start, value_end):
    "Parse paper attributes"

    # Check lists of positions, should be of equal size
    if not len(value_start) == len(value_end):
        raise RuntimeError("Syntax error in BibTeX file, unbalanced braces.")

    # Extract attributes and values
    paper = {}
    for i in range(len(value_start)):

        # Extract attribute
        if i == 0:
            attribute = block[0:value_start[0]]
        else:
            attribute = block[value_end[i - 1] + 1:value_start[i]]
        match = _attribute_pattern.search(attribute)
        if match is None:
            raise RuntimeError("Syntax error in BibTeX file, missing attribute name.")
        groups = match.groups()
        attribute = groups[0].lower()

        # Extract value
        value = block[value_start[i] + 1:value_end[i]].replace("\r", " ").replace("\n", " ").strip()

        # Set attribute and value
        paper[attribute] = value

    # Return a dictionary containing information about one paper
    return paper

def _check_paper(paper):
    "Check required attributes"

    # TODO: Do this during parsing, so we can give error messages with line number and text

    print("Found paper: %s" % pstr(paper))

    invalid = False

    # Check that paper has all required attributes
    entry_type = paper["entrytype"]
    key = paper["key"]
    attributes = config.get("entrytype_attributes")[entry_type]
    for attribute in attributes:
        # Check if the required field is a tuple and at least one field is used
        if isinstance(attribute, tuple):
            if not len([f for f in attribute if f in paper]) >= 1:
                print('  Missing required attribute(s) "%s" for paper "%s"' % ('"/"'.join(attribute), key))
                invalid = True
        elif not attribute in paper:
            print('  Missing required attribute "%s" for paper "%s"' % (attribute, key))
            invalid = True

    if invalid:
        paper["invalid"] = True
        print("  Skipping paper. Correct the above error(s) and import the paper again.")
        if not config.get("autofix"):
            input("  Press return to continue.")

def _extract_authors(paper, attribute):
    "Extract authors as tuple from string"

    names = paper[attribute].split(" and ")

    authors = []
    for name in names:
        name = name.strip()

        # Handle case Last, First
        if "," in name:
            words = name.split(",")
            if not len(words) == 2:
                paper["invalid"] = True
                print("  Incorrectly formatted author string:", name)
                if config.get("autofix"):
                    print("  Skipping paper.")
                else:
                    input("  Skipping paper, press return to continue.")
            words.reverse()
            name = " ".join([w.strip() for w in words])

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

    paper[attribute] = authors

def _extract_category(paper):
    "Extract category for paper"

    # Check if category is supported
    entry_type = paper["entrytype"]
    entrytype2category = config.get("entrytype2category")
    if not entry_type in entrytype2category:
        raise RuntimeError('Entry type "%s" not supported.' % entry_type)

    # Check default mapping
    category = entrytype2category[entry_type]
    if not category is None:
        return category

    # Special case: book or edited
    if entry_type == "book":
        if "editor" in paper:
            paper["author"] = paper["editor"]
            del paper["editor"]
            return "edited"
        else:
            return "books"

    # Special case: phdthesis
    if entry_type == "phdthesis":
        paper["thesistype"] = "phd"
        return "theses"

    # Special case: mscthesis
    if entry_type == "mastersthesis":
        paper["thesistype"] = "msc"
        return "theses"

    # Special case: misc
    if entry_type == "misc":
        if "code" in paper:
            return "courses"
        elif "meeting" in paper:
            return "talks"
        else:
            return "misc"

    raise RuntimeError("Unhandled special case for BibTeX entry type.")


def _skip_spaces(position, text) :
    "Get position of first character after position, not beeing a white space"
    while  position < len(text)-1 and text[position].isspace() :
        position += 1

    return position

def _get_line(position, text) :
    "Get the string with linenumber and text of the line that text[position] belongs to"

    # count newlines before position to get the linenumber
    newlines = text.count("\n", 0, position) + 1

    start = text[:position].rfind("\n")
    end   = text[position:].find("\n")
    return "(%d) : %s" % (newlines, text[start:position+end].strip())
