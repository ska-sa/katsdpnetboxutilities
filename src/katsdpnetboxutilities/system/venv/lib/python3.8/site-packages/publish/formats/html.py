"This module implements output for HTML."
from builtins import range

__author__ = "Anders Logg <logg@simula.no>"
__date__ = "2009-07-31 -- 2009-08-18"
__copyright__ = "Copyright (C) 2009 Anders Logg"
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

    # Get formatting rule
    html_format = config.get("html_format")

    # Get PDF directory
    pdf_dir = config.get("pdf_dir")

    # Iterate over categories
    current_paper = 0
    for category in categories:

        # Extract papers in category
        category_papers = [paper for paper in papers if paper["category"] == category]
        if len(category_papers) == 0:
            continue

        # Sort the list
        if sort_func is not None :
          category_papers.sort(key=sort_func)

        # Add internal links to each category
        if config.get("html_add_internal_links") :
            prefix += "<li><a href=\"#%s_id_%s\">%s</a></li>\n" % (config.get("html_class_prefix"),
                                                                 category,
                                                                 category_headings[category])

        # Write category
        text += '<h2 id="%s_id_%s">%s</h2>\n\n' % ( config.get("html_class_prefix"),
                                                    category,
                                                    category_headings[category])
        text += "<ol class=\"%s_list\">\n\n" %  config.get("html_class_prefix")

        # Iterate over papers in category
        for paper in category_papers:

            # Format paper entry
            paper_entry = html_format[category](paper)

            # Filter entry from special characters
            paper_entry = _filter(paper_entry)

            # Set directory to papers (a bit of a hack)
            paper_entry = paper_entry.replace("papers/", pdf_dir + "/")

            # Write entry for paper
            text += "<li class=\"publish_item\">\n" + paper_entry + "</li>\n"

        # Write end of list
        text += "</ol>\n"

    prefix = "<ul>" + prefix + "</ul>\n"

    return prefix+"\n"+text

def _filter(s):
    "Filter string for special characters."

    # List of replacements
    replacements = [("--", "&ndash;"),
                    ("\\ae", "ae"),
                    ("$", ""),
                    ("\\mathrm", ""),
                    ('\\aa', '&aring;'),
                    ('\\AA', '&Aring;'),
                    ('\\"a', '&auml;'),
                    ('\\"A', '&Auml;'),
                    ('\\"o', '&ouml;'),
                    ('\\"O', '&Ouml;'),
                    ('\\o',  '&oslash;'),
                    ('\\O',  '&Oslash;'),
                    ('\\&',   '&amp;'),
                    ('\\textonesuperior', "<sup>1</sup>"),
                    ('\\textendash', "&ndash;"),
                    ('\\textemdash', "&mdash;"),
                    ('\\textasciiacute', "&acute;"),
                    ('\\\'a', "&acute;"),
                    ('\\"u', "&uuml;"),
                    ('\\epsilon', "&epsilon;"),
                    ('\\\'\i', "&iacute;"),
                    ('\\textquoteright', "&apos;"), # Is this correct?
                    ('\\textquoteleft', "&apos;"), # Is this correct?
                    ("\\'", "&apos;"),
                    ("\l", "&#0322;"),
                    ("\\.Z", "&#379;"),
                    ("\\beta", "&beta;"),
                    ("\\r a", "&aring;"), # Note that order matters here
                    ("\\r", "&aring;"),   # and here
                    ("\`a", "&agrave;")
                    ]

    # Sort wrt to length of string
    replacements.sort(key=len, reverse=True)

    # Remove { }
    while (True) :
        found = False
        for i in range(len(s)) :
            if s[i] in ["{", "}"] and (i == 0 or s[i-1] != "\\") :
                found = True
                s = s[:i] + s[i+1:]
                break
        if not found :
            break

    # Iterate over replacements
    for (a, b) in replacements:
        s = s.replace(a, b)

    return s
