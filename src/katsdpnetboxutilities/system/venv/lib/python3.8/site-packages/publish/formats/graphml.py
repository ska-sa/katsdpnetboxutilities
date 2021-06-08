# -*- coding: utf-8 -*-
"This module implements output for Graph ML files where authors are nodes and joint work are edges."
from future import standard_library
standard_library.install_aliases()
from builtins import str


# See https://gephi.org/users/supported-graph-formats/graphml-format/ for some more details
__author__    = "Benjamin Kehlet <benjamik@simula.no>"
__date__      = "2012-01-08 -- 2012-01-08"
__copyright__ = "Copyright (C) 2012 Benjamin Kehlet"
__license__   = "GNU GPL version 3 or any later version"

import lxml.etree as xml
import io
import itertools
from publish import config


def write(papers) :
  # Dictionary mapping author name to id and counter
  authors = {}

  # Dictionary mapping tuple of author ids to counter
  edges = {}
  for paper in papers :
    for author in paper["author"] :
      if author in authors :
        authors[author]["count"] += 1
      else : 
        authors[author] = {'id' : len(authors), 'count' : 1}


    # sort the authors to ensure the order will not cause duplicates
    authors_sorted = sorted(paper["author"])
    for author_tuple in itertools.combinations(authors_sorted, 2) :
      # look up author id and create tuple
      author_ids = tuple( [authors[single_author]["id"] for single_author in author_tuple] )

      # increment counter or add entry
      if author_ids in edges :
        edges[author_ids]  += 1 
      else :
        edges[author_ids]  = 1
  
  xml_root = xml.Element("graphml")
  
  weight_element = xml.Element("key")
  weight_element.attrib["id"] = "weight_key"
  weight_element.attrib["for"] = "edge"
  weight_element.attrib["attr.name"] = "weight"
  weight_element.attrib["attr.type"] = "double"
  xml_root.append(weight_element)

  label_element = xml.Element("key")
  label_element.attrib["id"] = "label_key"
  label_element.attrib["for"] = "node"
  label_element.attrib["attr.name"] = "label"
  label_element.attrib["attr.type"] = "string"
  xml_root.append(label_element)

  publications_element = xml.Element("key")
  publications_element.attrib["id"] = "publications_key"
  publications_element.attrib["for"] = "node"
  publications_element.attrib["attr.name"] = "publications"
  publications_element.attrib["attr.type"] = "integer"
  xml_root.append(publications_element)

  if len(config.get("mark_author")) :
    marked_element = xml.Element("key")
    marked_element.attrib["id"] = "marked_key"
    marked_element.attrib["for"] = "node"
    marked_element.attrib["attr.name"] = "marked"
    marked_element.attrib["attr.type"] = "integer"
    default_element = xml.Element("default")
    default_element.text = "0"
    marked_element.append(default_element)
    xml_root.append(marked_element)

 
  root_element = xml.Element("graph")
  root_element.attrib["edgedefault"] = "undirected"
  xml_root.append(root_element)
  

  for author, author_data in authors.items() :
    node = xml.Element("node")
    node.attrib["id"] = str(author_data["id"])
    label = xml.Element("data")
    label.attrib["key"] = "label_key"
    label.text = _filter(author)
    node.append(label)
    publications = xml.Element("data")
    publications.attrib["key"] = "publications_key"
    publications.text = str(author_data["count"])

    # Mark author if requested
    if author.strip() in config.get("mark_author") :
      marked_data = xml.Element("data")
      marked_data.attrib["key"] = "marked_key"
      marked_data.text = "1"
      node.append(marked_data)

    node.append(publications)
    root_element.append(node)

  for (i, ((source, target), count)) in enumerate(edges.items()) :
    edge = xml.Element("edge")
    edge.attrib["source"] = str(source)
    edge.attrib["target"] = str(target)
    edge.attrib["id"] = str(i)
    weight = xml.Element("data")
    weight.attrib["key"] = "weight_key"
    weight.text = str(count)
    edge.append(weight)
    root_element.append(edge)

  return xml.tostring(xml_root, encoding="utf-8", xml_declaration=True, pretty_print=True)


def _filter(s):
    "Filter string for special characters."

    s = str(s, "utf-8")


    # List of replacements
    replacements = [("--", u'-'),
                    ("$", u""),
                    ("\\mathrm", u""),
                    ('\\aa', u'å'),
                    ('\\AA', u'Å'),
                    ('\\"a', u'ä'),
                    ('\\"A', u'Ä'),
                    ('\\"o', u'ö'),
                    ('\\"O', u'Ö'),
                    ('\\o',  u'ø'),
                    ('\\O',  u'ø'),
                    ('\\ae', u'æ'),
                    ('\\AE', u'Æ'),
                    ('\\&',  u'&'),
                    # ('\\textonesuperior', "<sup>1</sup>"),
                    ('\\textendash', u'-'),
                    ('\\textemdash', u'-'),
                    ('\\textasciiacute', u'\xb4'),
                    ('\\\'a', u'\xb4'),
                    ('\\"u', u'ü'),
                    #('\\epsilon', "&epsilon;"),
                    ('\\\'\i', u'í'),
                    # ('\\textquoteright', "&apos;") # Is this correct?
                    ]

    with_brackets = [ ("{"+a+"}", b) for (a, b) in replacements]
    replacements = with_brackets+replacements


    # Iterate over replacements
    for (a, b) in replacements :
        s = s.replace(a, b)

    return s
