"This module controls formatting for LaTeX and HTML."
from builtins import str

__author__    = "Anna Logg (anna@loggsystems.se)"
__date__      = "2008-11-17 -- 2009-07-31"
__copyright__ = "Copyright (C) 2008-2009 Anna Logg"
__license__   = "GNU GPL version 3 or any later version"

# Modified by Anders Logg, 2009.
# Modified by Benjamin Kehlet, 2010-2014.

from publish.common import short_author
from publish import config

#------------------------------------------------------------------------------
# LaTeX formatting
#------------------------------------------------------------------------------

def latex_format_articles(paper):
    "Return string for article in LaTeX format"

    text = []

    # authors
    text.append("%s. " %_latex_format_authors(_latex_get_authors_string(paper["author"])))

    # title
    text.append("%s.\n" % paper["title"])

    # journal
    journal_in_italic = "\\textit{%s}" % paper["journal"]
    text.append("%s" % _format_venue(journal_in_italic, paper["journal"], paper))

    # volume
    if "volume" in paper and paper["volume"].strip() :
        text.append(", vol. %s" % paper["volume"])
        if "number" in paper and paper["number"].strip() :
            text.append("(%s)" % paper["number"])

    # pages
    if "pages" in paper and paper["pages"].strip() :
        text.append(", pp. %s" %  paper["pages"])

    # year
    text.append(", %s." % paper["year"])

    return "".join(text)

def latex_format_books(paper):
    "Return string for book in LaTeX format"
    values = []

    # authors
    values.append("%s.\n" % _latex_format_authors(_latex_get_authors_string(paper["author"])))

    # title
    values.append(paper["title"])

    # edition
    if "edition" in paper :
        values += [", %s edition" % paper["edition"]]

    # publisher
    values.append(", \\textit{%s}" % paper["publisher"])

    # year
    values.append(", %s." % paper["year"])

    return "".join(values)

def latex_format_edited(paper):
    "Return string for edited book in LaTeX format"
    values = []
    values += ["%s. " % _latex_format_authors(_latex_get_authors_string(paper["author"]))]
    values += ["%s, " % paper["title"]]
    values += ["\\textit{%s}, " % paper["publisher"]]
    values += [paper["year"]+"."]
    return "\n".join(values)

def latex_format_chapters(paper):
    "Return string for chapter in LaTeX format"

    values = []

    # authors
    values.append("%s. " %_latex_format_authors(_latex_get_authors_string(paper["author"])))

    # title
    values.append(paper["title"])

    # book title
    values.append(". %s, " % _format_venue("\\textit{%s}" % paper["booktitle"], paper["booktitle"], paper, add_in=True))

    #editor
    if "editor" in paper :
        values.append("edited by %s, " % _latex_get_authors_string(paper["editor"]))

    # publisher
    values.append("%s, " % paper["publisher"])

    #if "chapter" in paper: values += [" chapter %s" % paper["chapter"]]
    #if "pages" in paper: values += [" pp. %s" % _format_pages(paper["pages"])]

    values.append(" %s." % paper["year"])
    return "".join(values)

def latex_format_proceedings(paper):
    "Return string for proceeding in LaTeX format"
    values = []

    # authors
    values.append("%s. " % _latex_format_authors(_latex_get_authors_string(paper["author"])))

    # title
    values.append(paper["title"])

    # book title
    values.append(". %s, " % _format_venue("\\textit{%s}" % paper["booktitle"], paper["booktitle"], paper, add_in=True))

    # year
    values.append(paper["year"])

    return "".join(values)

def latex_format_reports(paper):
    "Return string for report in LaTeX format"
    values = []

    # authors
    values.append("%s. " % _latex_format_authors(_latex_get_authors_string(paper["author"])))

    # title
    values.append(paper["title"])

    # institution
    values.append(", %s, " % paper["institution"])

    # year
    values.append(paper["year"])
    return "".join(values)

def latex_format_manuals(paper):
    "Return string for manual in LaTeX format"
    values = []

    # authors
    values.append("%s. " % _latex_format_authors(_latex_get_authors_string(paper["author"])))

    values.append(paper["title"])


    if "year" in paper: values += [", %s" % paper["year"]]
    return "".join(values)

def latex_format_theses(paper):
    "Return string for thesis in LaTeX format"
    values = []

    # authors
    values.append("%s. " %_latex_format_authors(_latex_get_authors_string(paper["author"])))

    # title
    values.append(paper["title"])

    #thesis type
    values.append(", %s" % config.get("thesistype_strings")[paper["thesistype"]])

    # school and year
    values.append(", %s, %s." % (paper["school"], paper["year"]))

    return "".join(values)

def latex_format_courses(paper):
    "Return string for course in LaTeX format"
    values = []
    values += [_latex_format_authors(_latex_get_authors_string(paper["author"]))]
    values += ["\\textit{%s}" % paper["title"]]
    values += ["(" + paper["code"] + ")"]
    values += [paper["institution"]]
    values += [paper["year"]]
    return _latex_join(values)

def latex_format_talks(paper):
    "Return string for talk in LaTeX format"
    values = []

    # author
    values.append("%s. " % _latex_format_authors(_latex_get_authors_string(paper["author"])))

    #title
    values.append(paper["title"])

    # meeting
    if "meeting" in paper :
        values.append(", %s" % paper["meeting"])

    #year
    values.append(", %s." % paper["year"])

    return "".join(values)

def latex_format_posters(paper):
    "Return string for poster in LaTeX format"
    values = []

    # author
    values.append("%s. " % _latex_format_authors(_latex_get_authors_string(paper["author"])))

    #title
    values.append(paper["title"])

    # meeting
    if "meeting" in paper :
        values.append(", %s" % paper["meeting"])

    #year
    values.append(", %s." % paper["year"])

    return "".join(values)

def latex_format_publicoutreach(paper):
    "Return string for public outreach in LaTeX format"
    values = []

    # author
    values.append("%s. " % _latex_format_authors(_latex_get_authors_string(paper["author"])))

    #title
    values.append(paper["title"])

    # meeting
    if "meeting" in paper :
        values.append(", %s" % paper["meeting"])

    #year
    values.append(", %s." % paper["year"])

    return "".join(values)

def latex_format_preprint(paper):
    "Return string for preprint in LaTeX format"
    values = []

    # authors
    values.append("%s. " % _latex_format_authors(_latex_get_authors_string(paper["author"])))

    # title
    values.append(paper["title"])

    # title
    values.append(", %s" % paper["year"])
    return "".join(values)

def latex_format_misc(paper):
    "Return string for misc in LaTeX format"
    values = []
    values += [_latex_format_authors(_latex_get_authors_string(paper["author"]))]
    values += ["\\textit{%s}" % paper["title"]]
    if "booktitle" in paper: values += ["in \\textit{%s}" % paper["booktitle"]]
    if "howpublished" in paper: values += [paper["howpublished"]]
    if "meeting" in paper: values += [paper["meeting"]]
    if "thesistype" in paper: values += [config.get("thesistype_strings")[paper["thesistype"]]]
    if "school" in paper: values += [paper["school"]]
    if "chapter" in paper: values += ["chapter %s" % paper["chapter"]]
    if "volume" in paper: values += ["vol. %s" % paper["volume"]]
    if "pages" in paper: values += ["pp. %s" % _latex_format_pages(paper["pages"])]
    if "year" in paper: values += [paper["year"]]
    return _latex_join(values)

def _latex_join(values):
    "Join values for LaTeX entry"
    return ",\n".join(values) + ".\n"

latex_format = {"articles"      : latex_format_articles,
                "books"         : latex_format_books,
                "edited"        : latex_format_edited,
                "chapters"      : latex_format_chapters,
                "proceedings"   : latex_format_proceedings,
                "refproceedings": latex_format_proceedings,
                "reports"       : latex_format_reports,
                "manuals"       : latex_format_manuals,
                "theses"        : latex_format_theses,
                "courses"       : latex_format_courses,
                "talks"         : latex_format_talks,
                "posters"       : latex_format_posters,
                "publicoutreach": latex_format_publicoutreach,
                "preprint"      : latex_format_preprint,
                "misc"          : latex_format_misc}

#------------------------------------------------------------------------------
# HTML formatting
#------------------------------------------------------------------------------

def html_format_articles(paper):
    "Return string for article in HTML format"
    values = []

    # Title
    values.append(_html_format_title(paper))

    # Author
    values.append(_html_get_authors_string(paper["author"]))

    # Journal
    values.append('<span class="%s_item_journal">%s</span>' % (config.get("html_class_prefix"), _format_venue(paper["journal"], paper["journal"], paper)))

    # Volume
    if "volume" in paper: values.append('<span class="%s_item_volum">vol. %s</span>' %  (config.get("html_class_prefix"), paper["volume"]))

    # Pages
    if "pages" in paper: values.append('<span class="%s_item_pages">pp. %s</span>' % (config.get("html_class_prefix"),
                                                                                      _html_format_pages(paper["pages"])))

    # Year
    values.append('<span class="%s_item_year">%s</span>' % (config.get("html_class_prefix"), paper["year"]))

    # DOI
    #if "doi" in paper: values.append('[<a href="http://dx.doi.org/%s">DOI:%s</a>]' % (paper["doi"], paper["doi"]))
    if "doi" in paper: values.append('[<a href="http://dx.doi.org/%s">DOI</a>]' % paper["doi"])

    # arXiv
    #if "arxiv" in paper: values.append('[<a href="http://arxiv.org/abs/%s">arXiv:%s</a>]' % (paper["arxiv"], paper["arxiv"]))
    if "arxiv" in paper: values.append('[<a href="http://arxiv.org/abs/%s">arXiv</a>]' % paper["arxiv"])

    return _html_join(values)

def html_format_books(paper):
    "Return string for book in HTML format"
    values = []
    values += [_html_format_title(paper)]
    values += [_html_get_authors_string(paper["author"])]
    values += ['<span class="%s_item_publisher">%s</span>' % (config.get("html_class_prefix"), paper["publisher"])]

    values.append('<span class="%s_item_year">%s</span>' % (config.get("html_class_prefix"), paper["year"]))
    return _html_join(values)

def html_format_edited(paper):
    "Return string for edited book in HTML format"
    values = []
    values += [_html_format_title(paper)]
    values += [_html_get_authors_string(paper["author"])]
    values += ['<span class="%s_item_publisher">%s</span>' % (config.get("html_class_prefix"), paper["publisher"])]
    values.append('<span class="%s_item_year">%s</span>' % (config.get("html_class_prefix"), paper["year"]))

    return _html_join(values)

def html_format_chapters(paper):
    "Return string for chapter in HTML format"
    values = []
    values += [_html_format_title(paper)]
    values += [_html_get_authors_string(paper["author"])]
    values += ['in <span class="%s_item_publisher">%s</span>' % (config.get("html_class_prefix"), paper["booktitle"])]
    if 'editor' in paper : values += [_html_format_editors(paper["editor"])]
    values += ['<span class="%s_item_publisher">%s</span>' % (config.get("html_class_prefix"), paper["publisher"])]
    if "chapter" in paper: values += ["chapter %s" % paper["chapter"]]
    if "pages" in paper: values += ["pp. %s" % _html_format_pages(paper["pages"])]

    values.append('<span class="%s_item_year">%s</span>' % (config.get("html_class_prefix"), paper["year"]))

    return _html_join(values)

def html_format_proceedings(paper):
    "Return string for proceeding in HTML format"
    values = []
    values += [_html_format_title(paper)]
    values += [_html_get_authors_string(paper["author"])]
    values += ['in <span class="%s_item_booktitle">%s</span>' % (config.get("html_class_prefix"), paper["booktitle"])]

    values.append('<span class="%s_item_year">%s</span>' % (config.get("html_class_prefix"), paper["year"]))
    return _html_join(values)

def html_format_reports(paper):
    "Return string for report in HTML format"
    values = []
    values += [_html_format_title(paper)]
    values += [_html_get_authors_string(paper["author"])]
    values += [paper["institution"]]

    values.append('<span class="%s_item_year">%s</span>' % (config.get("html_class_prefix"), paper["year"]))
    return _html_join(values)

def html_format_manuals(paper):
    "Return string for manual in HTML format"
    values = []
    values += [_html_format_title(paper)]
    values += [_html_get_authors_string(paper["author"])]
    if "year" in paper: values += [paper["year"]]
    return _html_join(values)

def html_format_theses(paper):
    "Return string for thesis in HTML format"
    values = []
    values += [_html_format_title(paper)]
    values += [_html_get_authors_string(paper["author"])]
    values += [config.get("thesistype_strings")[paper["thesistype"]]]
    values += [paper["school"]]

    values.append('<span class="%s_item_year">%s</span>' % (config.get("html_class_prefix"), paper["year"]))
    return _html_join(values)

def html_format_courses(paper):
    "Return string for course in HTML format"
    values = []
    values += [_html_format_title(paper)]
    values += [_html_get_authors_string(paper["author"])]
    values += [_html_get_authors_string(paper["author"])]
    values += [paper["institution"]]

    values.append('<span class="%s_item_year">%s</span>' % (config.get("html_class_prefix"), paper["year"]))
    return _html_join(values)

def html_format_talks(paper):
    "Return string for talk in HTML format"
    values = []
    values += [_html_format_title(paper)]
    values += [_html_get_authors_string(paper["author"])]
    if "meeting" in paper :
        values += ['<span class="%s_item_meeting">%s</span>' % (config.get("html_class_prefix"), paper["meeting"])]

    values.append('<span class="%s_item_year">%s</span>' % (config.get("html_class_prefix"), paper["year"]))
    return _html_join(values)

def html_format_posters(paper):
    "Return string for poster in HTML format"
    values = []
    values += [_html_format_title(paper)]
    values += [_html_get_authors_string(paper["author"])]
    values += ['<span class="%s_item_meeting">%s</span>' % (config.get("html_class_prefix"), paper["meeting"])]

    values.append('<span class="%s_item_year">%s</span>' % (config.get("html_class_prefix"), paper["year"]))
    return _html_join(values)



def html_format_preprint(paper):
    "Return string for preprint in HTML format"
    values = []
    values += [_html_format_title(paper)]
    values += [_html_get_authors_string(paper["author"])]
    if "year" in paper: values += [paper["year"]]
    return _html_join(values)

def html_format_publicoutreach(paper):
    "Return string for public outreach in HTML format"
    values = []
    values += [_html_format_title(paper)]
    values += [_html_get_authors_string(paper["author"])]
    values += ['<span class="%s_item_meeting">%s</span>' % (config.get("html_class_prefix"), paper["meeting"])]

    values.append('<span class="%s_item_year">%s</span>' % (config.get("html_class_prefix"), paper["year"]))
    return _html_join(values)

def html_format_misc(paper):
    "Return string for misc in HTML format"
    values = []
    values += [_html_format_title(paper)]
    values += [_html_get_authors_string(paper["author"])]
    if "howpublished" in paper:
        howpublished = paper["howpublished"]
        if "http://" in howpublished and "<a href" not in values[0]:
            link = ("http://" + howpublished.split("http://")[-1]).strip()
            values[0] = '<a href="%s">%s</a>' % (link, values[0])
        else:
            values += [howpublished]
    if "booktitle" in paper: values += ["in <i>%s</i>" % paper["booktitle"]]
    if "meeting" in paper: values += [paper["meeting"]]
    if "thesistype" in paper: values += [config.get("thesistype_strings")[paper["thesistype"]]]
    if "school" in paper: values += [paper["school"]]
    if "chapter" in paper: values += ["chapter %s" % paper["chapter"]]
    if "volume" in paper: values += ["vol. %s" % paper["volume"]]
    if "pages" in paper: values += ["pp. %s" % _html_format_pages(paper["pages"])]
    if "year" in paper: values.append('<span class="%s_item_year">%s</span>' % (config.get("html_class_prefix"), paper["year"]))
    return _html_join(values)

def _html_format_title(paper):
    "Format title for HTML, with or without link to PDF file"

    if paper["category"] == "courses":
        title = "%s (%s)" % (paper["title"], paper["code"])
    else:
        title = paper["title"]

    if "pdf" in paper and not paper["pdf"] == "missing":
        return '<span class="publish_item_title"><a href=\"%s\">%s</a></span>' % (paper["pdf"], title)
    else:
        return '<span class="publish_item_title">%s</span>' % title

def _html_format_editors(authors):
    "Convert editor tuple to author string"
    return '<span class="publish_item_editors">Edited by %s</span>' % _html_get_authors_string(authors)

def _html_get_authors_string(authors):
    "Convert author tuple to author string"
    authors = [_html_mark_author(author, short_author(author).strip()) for author in authors]
    if len(authors) == 1:
        str = authors[0]
    else :
        if authors[-1] == "others":
            str =  ", ".join(authors[:-1]) + " et al."
        else:
            str = ", ".join(authors[:-1]) + " and " + authors[-1]

    return '<span class="%s_item_authors">%s</span>' % (config.get("html_class_prefix"), str)

def _html_mark_author(author, text) :
  "Mark the text with bold face if author is in the list of marked authors"

  if author.strip() in config.get("mark_author") :
    return "<strong>%s</strong>" % text

  else :
    return text

def _html_format_pages(pages):
    "Format pages"
    if "--" in pages: return pages.replace("--", "&mdash;")
    else :            return pages.replace("-", "&mdash;")

def _html_join(values):
    "Join values for HTML entry"
    entry = "<br>\n".join(values[:2]) + "<br>\n" + ", ".join(values[2:]) + "\n"
    entry = entry.replace("{", "")
    entry = entry.replace("}", "")
    return entry

html_format = {"articles"      : html_format_articles,
               "books"         : html_format_books,
               "edited"        : html_format_edited,
               "chapters"      : html_format_chapters,
               "proceedings"   : html_format_proceedings,
               "refproceedings": html_format_proceedings,
               "reports"       : html_format_reports,
               "manuals"       : html_format_manuals,
               "theses"        : html_format_theses,
               "courses"       : html_format_courses,
               "talks"         : html_format_talks,
               "posters"       : html_format_posters,
               "preprint"      : html_format_preprint,
               "publicoutreach": html_format_publicoutreach,
               "misc"          : html_format_misc}

#------------------------------------------------------------------------------
# reSt formatting
#------------------------------------------------------------------------------

def rst_format_articles(paper):
    "Return string for article in reSt format"
    values = []

    # Author
    values.append(_rst_get_authors_string(paper))

    # Title
    values.append(_rst_format_title(paper))

    # Journal
    values.append(_format_venue(paper["journal"], paper["journal"], paper))

    # Volume
    if "volume" in paper:
        vol = paper["volume"]
        if "number" in paper :
            vol += "(%s)" % paper["number"]
        values.append(vol)

    # Pages
    if "pages" in paper:
        values.append(_rst_format_pages(paper["pages"]))

    # DOI
    if "doi" in paper:
        values.append(_rst_format_doi(paper["doi"]))

    # arXiv
    if "arxiv" in paper:
        values.append(_rst_format_arxiv(paper["arxiv"]))

    return _rst_join(values)

def rst_format_books(paper):
    "Return string for book in reSt format"
    values = []
    values += [_rst_get_authors_string(paper)]
    values += [_rst_format_title(paper)]
    values += [paper["publisher"]]
    if "doi" in paper: values.append(_rst_format_doi(paper["doi"]))
    return _rst_join(values)

def rst_format_edited(paper):
    "Return string for edited book in reSt format"
    values = []
    values += [_rst_get_authors_string(paper)]
    values += [_rst_format_title(paper)]
    values += [paper["publisher"]]
    return _rst_join(values)

def rst_format_chapters(paper):
    "Return string for chapter in reSt format"
    values = []
    values += [_rst_get_authors_string(paper)]
    values += [_rst_format_title(paper)]
    values += [paper["booktitle"]]
    #values += [_rst_format_editors(paper)]
    values += [paper["publisher"]]
    if "chapter" in paper: values += ["Chapter %s" % paper["chapter"]]
    if "pages" in paper: values += ["pp. %s" % _rst_format_pages(paper["pages"])]
    return _rst_join(values)

def rst_format_proceedings(paper):
    "Return string for proceeding in reSt format"
    values = []
    values += [_rst_get_authors_string(paper)]
    values += [_rst_format_title(paper)]
    values += [paper["booktitle"]]
    return _rst_join(values)

def rst_format_reports(paper):
    "Return string for report in reSt format"
    values = []
    values += [_rst_get_authors_string(paper)]
    values += [_rst_format_title(paper)]
    values += [paper["institution"]]
    values += [paper["number"]]
    return _rst_join(values)

def rst_format_manuals(paper):
    "Return string for manual in reSt format"
    values = []
    values += [_rst_get_authors_string(paper)]
    values += [_rst_format_title(paper)]
    if "year" in paper: values += [paper["year"]]
    return _rst_join(values)

def rst_format_theses(paper):
    "Return string for thesis in reSt format"
    values = []
    values += [_rst_get_authors_string(paper)]
    values += [_rst_format_title(paper)]
    values += [config.get("thesistype_strings")[paper["thesistype"]]]
    values += [paper["school"]]
    values += [paper["year"]]
    return _rst_join(values)

def rst_format_courses(paper):
    "Return string for course in reSt format"
    values = []
    values += [_rst_get_authors_string(paper)]
    values += [_rst_format_title(paper)]
    values += [paper["institution"]]
    values += [paper["year"]]
    return _rst_join(values)

def rst_format_talks(paper):
    "Return string for talk in reSt format"
    values = []
    values += [_rst_get_authors_string(paper)]
    values += [_rst_format_title(paper)]
    values += [paper["meeting"]]
    values += [paper["year"]]
    return _rst_join(values)

def rst_format_posters(paper):
    "Return string for poster in reSt format"
    values = []
    values += [_rst_get_authors_string(paper)]
    values += [_rst_format_title(paper)]
    values += [paper["meeting"]]
    values += [paper["year"]]
    return _rst_join(values)


def rst_format_misc(paper):
    "Return string for misc in reSt format"
    values = []
    values += [_rst_get_authors_string(paper)]
    values += [_rst_format_title(paper)]
    if "howpublished" in paper:
        howpublished = paper["howpublished"]
        values += [howpublished]
    if "booktitle" in paper: values += ["in *%s*" % paper["booktitle"]]
    if "meeting" in paper: values += [paper["meeting"]]
    if "thesistype" in paper: values += [config.get("thesistype_strings")[paper["thesistype"]]]
    if "school" in paper: values += [paper["school"]]
    if "chapter" in paper: values += ["Chapter %s" % paper["chapter"]]
    if "volume" in paper: values += ["vol. %s" % paper["volume"]]
    if "pages" in paper: values += ["pp. %s" % _rst_format_pages(paper["pages"])]
    if "year" in paper: values.append(paper["year"])
    return _rst_join(values)

def _rst_format_title(paper):
    "Format title for reSt, with or without link to PDF file"
    if paper["category"] == "courses":
        title = "%s (%s)" % (paper["title"], paper["code"])
    else:
        title = paper["title"]
    return "*%s*" % title

def _rst_format_editors(paper):
    "Convert editor tuple to author string"
    return "Edited by %s" % _rst_get_authors_string(paper)

def _rst_get_authors_string(paper):
    "Convert author tuple to author string"
    authors = paper["author"]
    authors = [_rst_mark_author(author, short_author(author).strip()) \
                   for author in authors]
    if len(authors) == 1:
        str = authors[0]
    else :
        if authors[-1] == "others":
            str =  ", ".join(authors[:-1]) + " et al."
        else:
            str = ", ".join(authors[:-1]) + " and " + authors[-1]
    str = "**%s (%s)**" % (str, paper["year"])
    return str

def _rst_mark_author(author, text) :
  "Mark the text with bold face if author is in the list of marked authors"
  if author.strip() in config.get("mark_author") :
    return "**%s**" % text
  else:
    return text

def _rst_format_pages(pages):
    "Format pages"
    if "--" in pages:
        pages = pages.replace("--", "-")
    return "pp. %s" % pages

def _rst_format_doi(doi):
    "Format DOI"
    return "[`doi:%s <http://dx.doi.org/%s>`_]" % (doi, doi)

def _rst_format_arxiv(arxiv):
    "Format arXiv"
    return "[`arXiv:%s <http://arxiv.org/abs/%s>`_]" % (arxiv, arxiv)

def _rst_join(values):
    "Join values for reSt entry"
    entry = "* " + values[0] + ".\n  " + ",\n  ".join(values[1:]) + "." + "\n"
    entry = entry.replace("{", "")
    entry = entry.replace("}", "")
    return entry

rst_format = {"articles"      : rst_format_articles,
              "books"         : rst_format_books,
              "edited"        : rst_format_edited,
              "chapters"      : rst_format_chapters,
              "proceedings"   : rst_format_proceedings,
              "refproceedings": rst_format_proceedings,
              "reports"       : rst_format_reports,
              "manuals"       : rst_format_manuals,
              "theses"        : rst_format_theses,
              "courses"       : rst_format_courses,
              "talks"         : rst_format_talks,
              "posters"       : rst_format_posters,
              "misc"          : rst_format_misc}

#------------------------------------------------------------------------------
# Utility functions
#------------------------------------------------------------------------------

def _latex_mark_author(author, text) :
  "Mark the text with bold face if author is in the list of marked authors"

  if author.strip() in config.get("mark_author") :
    return "\\textbf{%s}" % text

  else :
    return text

def _latex_format_authors(author_string) :
  if config.get("use_textsc") :
    return "\\textsc{%s}" % author_string
  else :
    return author_string

def _latex_get_authors_string(authors):
    "Convert author tuple to author string"
    authors = [_latex_mark_author(author, short_author(author).strip()) for author in authors]
    if len(authors) == 1:
        return authors[0]
    if authors[-1] == "others":
        return ", ".join(authors[:-1]) + " et al."
    else:
        return ", ".join(authors[:-1]) + " and " + authors[-1]

def _latex_format_editors(authors):
    "Convert editor tuple to author string"
    return "Edited by " + _latex_get_authors_string(authors)

def _latex_format_pages(pages):
    "Format pages"
    if "--" in pages: return pages
    return pages.replace("-", "--")

def _format_venue(formatted_venue, venue, paper, add_in=False):
    "Format venue"
    status = paper.get("status", "published")
    if status == "published":
        if add_in:
            return "In " + formatted_venue
        else:
            return formatted_venue
    elif status == "accepted":
        return "Accepted for publication in " + formatted_venue
    elif status == "submitted":
        #if venue == "none":
        #    return "Submitted to journal for publication"
        #else:
        #    return "Submitted to " + formatted_venue
        return "Submitted to journal for publication"
    else:
        return "(%s)" % str(status)
