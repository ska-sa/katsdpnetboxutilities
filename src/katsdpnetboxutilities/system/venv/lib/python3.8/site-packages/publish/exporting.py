"This module implements data export to different file formats."
from __future__ import print_function
from __future__ import absolute_import

__author__ = "Anna Logg (anna@loggsystems.se)"
__date__ = "2008-11-11 -- 2009-08-30"
__copyright__ = "Copyright (C) 2008-2009 Anna Logg"
__license__  = "GNU GPL version 3 or any later version"

# Last modified: 2011-12-05

# Modified by Anders Logg, 2009-2011.

from publish.importing import read_database
from publish import config
from .formats import bibtex, latex, pub, pdf, html, rst, graphml
from .validation import validate_papers
from .filtering import filter_papers
from .log import print_summary

def export_file(filename, filters=[]):
    "Export data into desired file format"

    # Make sure we don't overwrite the database
    database_filename = config.get("database_filename")
    if filename == database_filename:
        raise RuntimeError('Papers cannot be exported to the default database ("%s").' % database_filename)

    # Read database
    database_papers = read_database(database_filename)

    # Why should the database be validated on export?
    #(valid_papers, invalid_papers) = validate_papers(database_papers)

    # Filter papers
    filtered_papers = filter_papers(database_papers, filters)

    # Get the filename suffix
    suffix = filename.split(".")[-1]

    # Choose format based on suffix
    if suffix in ("bib", "bibtex"):
        write = bibtex.write
    elif suffix == "pub":
        write = pub.write
    elif suffix == "tex":
        write = latex.write
    elif suffix == "pdf":
        write = pdf.write
    elif suffix == "html":
        write = html.write
    elif suffix == "rst":
        write = rst.write
    elif suffix == "graphml" :
        write = graphml.write
    else:
        raise RuntimeError("Unknown file format.")

    # Open and read file
    text = write(filtered_papers)
    file = open(filename, "w")
    try:
        file.write(text)
    except UnicodeEncodeError as e:
        file.write(text.encode('utf-8'))
    except Exception as e:
        raise RuntimeError('Unable to write file "%s" (exception %s: %s)'
                           % (filename, type(e), e))
    file.close()

    # Print summary
    print_summary(filtered_papers)
    print("")
    print("Exported %d paper(s) to %s." % (len(filtered_papers), filename))
