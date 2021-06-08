# -*- coding: utf-8 -*-
"This module implements output for reStructuredText."


__author__ = "Anders Logg <logg@simula.no>"
__date__ = "2011-12-05 -- 2011-12-05"
__copyright__ = "Copyright (C) 2011 Anders Logg"
__license__  = "GNU GPL version 3 or any later version"

from publish import config

def write(papers, sort_func=None):
    "Format the given list of papers in HTML format."

    text = ""
    prefix = ""

    # Get the categories.
    # Assume unique names
    categories = config.get("categories")
    category_headings = config.get("category_headings")
    skip_categories = config.get("skip_categories")

    # Get formatting rule
    rst_format = config.get("rst_format")

    # Get PDF directory
    pdf_dir = config.get("pdf_dir")

    # Iterate over categories
    current_paper = 0
    if skip_categories:

        # Iterate over papers
        for paper in papers:

            # Format paper entry
            category = paper["category"]
            paper_entry = rst_format[category](paper)

            # Filter entry from special characters
            paper_entry = _filter(paper_entry)

            # Set directory to papers (a bit of a hack)
            paper_entry = paper_entry.replace("papers/", pdf_dir + "/")

            # Write entry for paper
            text += paper_entry + "\n"

    else:

        # Iterate over categories
        for category in categories:

            # Extract papers in category
            category_papers = [paper for paper in papers if paper["category"] == category]
            if len(category_papers) == 0:
                continue

            # Sort the list
            if sort_func is not None :
                category_papers.sort(sort_func)

            # Write category
            heading = category_headings[category]
            text += "%s\n" % heading
            text += "="*len(heading) + "\n\n"

            # Iterate over papers in category
            for paper in category_papers:

                # Format paper entry
                paper_entry = rst_format[category](paper)

                # Filter entry from special characters
                paper_entry = _filter(paper_entry)

                # Set directory to papers (a bit of a hack)
                paper_entry = paper_entry.replace("papers/", pdf_dir + "/")

                # Write entry for paper
                text += paper_entry + "\n"

    return text

def _filter(s):
    "Filter string for special characters."

    # List of replacements
    replacements = [("--", "&ndash;"),
                    ("$", ""),
                    ("\\mathrm", ""),
                    ('\\aa', 'å'),
                    ('\\AA', 'ä'),
                    ('\\"a', 'ä'),
                    ('\\"A', 'Ä'),
                    ('\\"o', 'ö'),
                    ('\\"O', 'Ö'),
                    ('\\o',  'ø'),
                    ('\\O',  'Ø'),
                    ('\\ae', 'æ'),
                    ('\\AE', 'Æ'),
                    ('\\&',   '&amp;'),
                    ('\\textonesuperior', "<sup>1</sup>"),
                    ('\\textendash', "&ndash;"),
                    ('\\textemdash', "&mdash;"),
                    ('\\textasciiacute', "&acute;"),
                    ('\\\'a', "&acute;"),
                    ('\\"u', "&Uuml;"),
                    ('\\epsilon', "&epsilon;"),
                    ('\\\'\i', "&iacute;"),
                    ('\\textquoteright', "&apos;") # Is this correct?
                    ]

    # Iterate over replacements
    for (a, b) in replacements:
        s = s.replace(a, b)

    return s
