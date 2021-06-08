"This module implements data import from different file formats."
from __future__ import print_function
from builtins import str
from builtins import range

__author__ = "Anna Logg (anna@loggsystems.se)"
__date__ = "2008-10-27 -- 2008-11-08"
__copyright__ = "Copyright (C) 2008 Anna Logg"
__license__  = "GNU GPL version 3 or any later version"

# Last changed: 2012-08-31

# Modified by Benjamin Kehlet 2012

from publish import config
from publish.common import pstr, is_duplicate, is_allowed_duplicate
from publish.algorithms import distance
from publish.interaction import ask_user_alternatives
from publish.formats import pub

def merge_papers(papers_0, papers_1):
    "Merge two lists of papers into one common list"

    print("")
    print("Merging papers")
    print("--------------")
    print("")
    print("Need to merge %d + %d = %d papers." % \
          (len(papers_0), len(papers_1), len(papers_0) + len(papers_1)))
    print("")

    # Concatenate lists and then check every paper against all others
    papers = papers_0 + papers_1

    merged_papers = process_duplicates(papers)

    return merged_papers


def process_duplicates(papers) :
    " Search for duplicates, ask user what to do, return processed list"

    merged_papers = []

    for paper in papers:

        # Look for close match
        (matching_paper, matching_position) = _find_matching_paper(paper, merged_papers)

        # Add paper if no match
        if matching_paper is None:
            merged_papers.append(paper)
            continue

        # Ignore exact duplicates
        if _exact_match(paper, matching_paper):
            print("Found exact duplicate paper %s, skipping." % pstr(paper))
            continue

        # Add paper if matching paper marked as duplicate
        # NOTE: The attribute "duplicate" is now superseded by "allowed_duplicates". 
        # "duplicate" will be read and respected when merging, but not written

        if is_duplicate(matching_paper):
            print("Warning: Attribute 'duplicate' is deprecated. Use 'allowed_duplicates' and specify keys of duplicates.")
            print("Found close match with allowed duplicate for paper %s, keeping paper.\n" % pstr(paper))
            merged_papers.append(paper)
            continue

        if is_allowed_duplicate(paper, matching_paper) :
            print("Found close match with allowed duplicate for paper %s, keeping paper.\n" % pstr(paper))
            merged_papers.append(paper)
            continue


        # Remove matching paper (so we can add back the merged paper)
        del merged_papers[matching_position]

        # Merge paper with matching paper
        print("Found close match between %s and %s, merging papers." % (pstr(paper), pstr(matching_paper)))        
        merged_paper = _merge_papers(matching_paper, paper)
        for p in merged_paper:
            merged_papers.append(p)

    return merged_papers

def _find_matching_paper(paper, merged_papers):
    "Find paper that is so similar that it is probably intended to be the same"

    min_distance = 1.0
    matching_paper = None
    matching_position = None
    matching_distance = config.get("matching_distance_strong")

    # Get venue type
    category = paper["category"]
    category_venues = config.get("category_venues")
    # "journal", "booktitle", etc
    venue_type = category_venues[category] if "category" in category_venues else None 

    # Compare against all papers
    for i in range(len(merged_papers)):

        p = merged_papers[i]

        # Handle the special case where one of the papers is a talk
        if ((paper["category"] == "talks" or p["category"] == "talks") and
            paper["category"] != p["category"] and config.get("talks_dont_duplicate")) :
            continue

        # Compute venue distance
        if venue_type is None or not p["category"] == category:
            d_venue = 0
        else:
            d_venue = distance(paper[venue_type].lower(), p[venue_type].lower())

        # Compute title distance
        d_title = distance(paper["title"].lower(), p["title"].lower())

        # Compute overall distance
        d = max(d_venue, d_title)

        # Check for match
        if d < matching_distance and d < min_distance:
            min_distance = d
            matching_paper = p
            matching_position = i

    return (matching_paper, matching_position)

def _exact_match(paper0, paper1):
    "Check if papers match exactly."

    ignores = ["duplicate", "invalid", "allowed_duplicates"]

    attributes = [attribute for attribute in paper0 if not attribute in ignores] + \
                 [attribute for attribute in paper1 if not attribute in ignores]

    for attribute in attributes:
        if not attribute in paper0 or not attribute in paper1:
            return False
        if not paper0[attribute] == paper1[attribute]:
            return False

    return True

def _merge_papers(paper0, paper1):
    "Merge papers"

    if "key" in paper0 and "title" in paper0:
        print("  " + paper0["key"] + ": " + paper0["title"])
    if "key" in paper1 and "title" in paper1:
        print("  " + paper1["key"] + ": " + paper1["title"])

    # Get all attributes to check
    common_attributes = []
    for attribute in paper0:
        if attribute in paper1:
            common_attributes.append(attribute)
    for attribute in paper1:
        if attribute in paper0 and attribute not in common_attributes:
            common_attributes.append(attribute)

    # Sort the attributes to make sure output is readable and consistent across
    # runs (otherwise regression tests will fail)
    common_attributes.sort()
    print(common_attributes)

    # Check all common attributes
    merged_paper = {}
    identical = True
    for attribute in common_attributes:
        value0 = paper0[attribute]
        value1 = paper1[attribute]
        if value0 == value1:
            merged_paper[attribute] = value0
        elif value0 == "":
            merged_paper[attribute] = value1
        elif value1 == "":
            merged_paper[attribute] = value0
        else:
            identical = False
            while True:
                alternative = ask_user_alternatives('  Attribute "%s" differs, what should I do?' % attribute,
                                                    ('Keep both papers (marking them as allowed duplicates).',
                                                     'Ignore papers (marking them as invalid).',
                                                     'Keep first paper (%s) and ignore second paper (%s)' % \
                                                     (pstr(paper0), pstr(paper1)),
                                                     'Keep second paper (%s) and ignore first paper (%s)' % \
                                                     (pstr(paper0), pstr(paper1)),
                                                     'Use attribute from first paper ("%s")' % str(value0),
                                                     'Use attribute from second paper ("%s")' % str(value1),
                                                     'Print diff.'))
                
                print("")
                if alternative == 0:
                    paper0["allowed_duplicates"] = [paper1["key"]] + (paper0["allowed_duplicates"] if "allowed_duplicates" in paper0 else [])
                    paper1["allowed_duplicates"] = [paper0["key"]] + (paper1["allowed_duplicates"] if "allowed_duplicates" in paper1 else [])

                    return [paper0, paper1]
                elif alternative == 1:
                    paper0["invalid"] = True
                    paper1["invalid"] = True
                    return [paper0, paper1]
                elif alternative == 2:
                    return [paper0]
                elif alternative == 3:
                    return [paper1]
                elif alternative == 4:
                    merged_paper[attribute] = value0
                    break
                elif alternative == 5:
                    merged_paper[attribute] = value1
                    break
                elif alternative == 6:
                    print(pub.write_diff(paper0, paper1))
                else:
                    raise RuntimeError("Unknown option.")

    if identical:
        print("  No conflicting attributes, merge ok.")
    
    # Add unique attributes from paper0
    for attribute in paper0:
        if not attribute in paper1:
            merged_paper[attribute] = paper0[attribute]
    for attribute in paper1:
        if not attribute in paper0:
            merged_paper[attribute] = paper1[attribute]

    return [merged_paper]
