"This module implements generation of paper keys (used by validation)."
from __future__ import print_function

__author__ = "Anders Logg (logg@simula.no)"
__date__ = "2009-06-30 -- 2009-06-30"
__copyright__ = "Copyright (C) 2009 Anders Logg"
__license__  = "GNU GPL version 3 or any later version"

from publish.common import pstr

def generate_keys(papers):
    "Generate keys for all papers (if not already existing)"

    # Set of used keys
    used_keys = set()

    # Iterate over all papers
    for paper in papers:

        # Skip paper if key is already present
        if "key" in paper:
            continue

        # Generate key
        key = _generate_key(paper, used_keys)
        key = _filter_key(key)
        used_keys.add(key)

        # Set key
        paper["key"] = key
        print("Adding key for paper %s: %s" % (pstr(paper), key))

    return papers

def _generate_key(paper, used_keys):
    """Generate key for paper. The following naming scheme is used:

      FooBar2007
      FooBar2009a
      FooBar2009b

    The letter prefix is always used even if there is only one paper
    for the authors that year (so keys don't need to be updated if
    a new paper is added).

    If there are more than two authors, EtAl is added.

    Keys for some categories are formatted differently:

      courses: <code>.<year>
      talks:   FooBar<date> (with any "-" removed to work with LaTeX)
    """

    # Special case: courses
    if paper["category"] == "courses":
        return paper["code"] + "." + paper["year"]

    # Generate basic key
    last_names = [author.split(" ")[-1] for author in paper["author"]]
    key = "".join(last_names[:min(len(last_names), 2)])
    if len(last_names) > 2:
        key += "EtAl"
    if paper["category"] == "talks" and "date" in paper :
        key += paper["date"].replace("-", "")
    else:
        key += paper["year"]

    # Add suffix until we find something unique
    letters = "abcdefghijklmnopqrstuvxyz"
    for letter in letters:
        if not (key + letter) in used_keys:
            key = key + letter
            break

    # Check that we found a unique key
    if key in used_keys:
        raise RuntimeError("""Too many papers, out of suffix letter. This is a known bug/feature which should
be easy to fix.""")

    return key

def _filter_key(key):
    "Filter key, removing special characters."

    key = key.replace("{", "")
    key = key.replace("}", "")
    key = key.replace("\\", "")

    return key
