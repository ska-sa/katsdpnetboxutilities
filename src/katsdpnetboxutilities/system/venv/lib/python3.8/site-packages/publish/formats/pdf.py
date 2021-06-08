"This module implements output for pdf."
from __future__ import absolute_import

__author__ = "Anna Logg (anna@loggsystems.se)"
__date__ = "2008-11-25 -- 2008-11-25"
__copyright__ = "Copyright (C) 2008 Anna Logg"
__license__  = "GNU GPL version 3 or any later version"

# Modified by Anders Logg 2011
# Last changed: 2012-06-02

from tempfile import mkstemp
from os import system

from publish import config
from . import latex

def write(papers, sort_func=None):
    "Format the given list of papers in the pdf format."

    # Start of pdf paper
    latex_text = ""
    latex_text += "\\documentclass[11pt]{article}\n"
    latex_text += "\\usepackage{textcomp}\n"
    latex_text += "\\usepackage{a4wide}\n"

    # Because of some font issues in latex, we need to include
    # this package if we are going to nest \textbf and and \textsc
    # \textbf is only used if we are going to mark specific authors
    if config.get("use_textsc") and len(config.get("mark_author")) > 0 :
        latex_text += "\\usepackage[T1]{fontenc}\n"
    latex_text += "\\usepackage{url}\n"
    latex_text += "\\begin{document}\n"

    # Get headline
    headline = config.get("headline")
    if headline == "": headline = "Publications"

    # Write headline
    repeat_headline = config.get("repeat_headline")
    if repeat_headline:
        latex_text += "\\renewcommand \\refname{%s}\n\n" % headline
    else:
        latex_text += "\\renewcommand \\refname{\\vspace{-0.7cm}}\n\n"
        latex_text += "\\section*{%s}\n\n" % headline

    # LaTeX output
    latex_text += latex.write(papers, sort_func)

    # End of pdf paper
    latex_text += "\\end{document}"

    # Write string to LaTeX file
    try:
        (handle, latex_filename) = mkstemp(".tex")
        latex_file = open(latex_filename, "w")
        latex_file.write(latex_text)
        latex_file.close()
    except:
        raise RuntimeError("Unable to generate intermediate LaTeX code for PDF output.")

    # FIXME: Specifying /tmp is platform-specific
    # FIXME: Remove temporary files

    # Run pdflatex on LaTeX file
    system("pdflatex -output-directory /tmp %s" % latex_filename)

    # Read PDF file
    try:
        pdf_filename = ".".join(latex_filename.split(".")[:-1]) + ".pdf"
        pdf_file = open(pdf_filename, "r")
        pdf_text = pdf_file.read()
        pdf_file.close()
    except:
        raise RuntimeError("Unable to read generated PDF output.")

    # Show PDF
    if config.get("view_pdf"):
        system("%s %s" % (config.get("pdf_viewer"), pdf_filename))

    return pdf_text
