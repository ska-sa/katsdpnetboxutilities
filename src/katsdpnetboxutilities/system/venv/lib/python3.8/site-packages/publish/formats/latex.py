"This module implements input/output for LaTeX."

__author__ = "Anna Logg (anna@loggsystems.se)"
__date__ = "2008-11-06 -- 2008-11-12"
__copyright__ = "Copyright (C) 2008 Anna Logg"
__license__  = "GNU GPL version 3 or any later version"

from publish import config


def write(papers, sort_func=None):
    "Format the given list of papers in the LaTeX format."

    text = ""

    # Get formatting rule
    latex_format = config.get("latex_format")
    compact = config.get("compact")
    global_numbering = config.get("global_numbering")
    use_labels = config.get("use_labels")
    category_labels = config.get("category_labels")

    # Start of LaTeX paper
    if global_numbering and not compact:
        text+= "\\begin{thebibliography}{99}\n"

    # Iterate over categories
    categories = config.get("categories")
    current_paper = 0
    for category in categories:
        # Extract papers in category
        category_papers = [paper for paper in papers if paper["category"] == category]
        if len(category_papers) == 0:
            continue

        # Sort the list
        if sort_func is not None :
          category_papers.sort(key=sort_func)

        # Write category
        category_headings = config.get("category_headings")
        if compact:
            text += "\n\\textit{%s}\n\n" % category_headings[category]
        else:
            text += "\\subsection*{%s}\n" % category_headings[category]

        if not global_numbering and not compact :
            text += "\\begin{thebibliography}{99}\n"

        # Iterate over papers in category
        for (counter, paper) in enumerate(category_papers):

            # Get key (or generate key)
            if "key" in paper:
                key = paper["key"]
            else:
                key = "paper%d" % current_paper

            entry_text = latex_format[category](paper)

            # Set bibitem key
            if use_labels:
                label = "[%s%d]" % (category_labels[category], counter + 1)
            else:
                label = ""

            # Write each paper as bibitem
            if compact:
                text += "[%d] %s\\\\[1ex]\n" % (current_paper, entry_text)
            else:
                text += "\\bibitem%s{%s} {%s}\n" % (label, key, entry_text)

            current_paper += 1

        if not global_numbering and not compact :
            text += "\\end{thebibliography}\n\n"


    if global_numbering and not compact:
        text += "\\end{thebibliography}"

    return text
