"""
Default configuration data for publish.

User can make a publish_config.py file with

from publish.config.default.py import *
"""

__author__ = "Anna Logg (anna@loggsystems.se)"
__date__ = "2008-10-28 -- 2008-11-03"
__copyright__ = "Copyright (C) 2008 Anna Logg"
__license__  = "GNU GPL version 3 or any later version"

MARKER_FOR_IMPORT_0123456789 = 'variable for marking import of this module'

# Modified by Anders Logg 2011
# Modified by Benjamin Kehlet 2012-2013
# Last modified: 2013-04-23

database_filename       = "papers.pub"
local_venues_filename   = "venues.list"
authornames_filename    = "authors.list"
invalid_filename_prefix = "invalid_papers"

matching_distance_strong = 0.1
matching_distance_weak   = 0.5

autofix  = False
debug    = False

pdf_viewer = "evince"
view_pdf = True
pdf_dir = "papers"

headline = ""
repeat_headline = False

compact = False

require_page_range = False
page_separator = "-"

# Set a prefix for the class names when generating html.
# Example: class="publish_item_title"
html_class_prefix = "publish"
html_add_internal_links = False

# Should numbering in report be global
# or start over for each category
# NOTE: Not fully implemented for all report types.
global_numbering = False

# Control whether output should contain categories or just be a list
# NOTE: Not fully implemented for all report types.
skip_categories = False

# Control whether LaTeX bibitems should use labels [J1], [J2] etc
# NOTE: Not fully implemented for all report types.
use_labels = False

# When searching for duplicates, handle the case where one publication
# is a talk and the other is not and a non-duplicate
# Usefull since we often have talks with the same title as a paper
talks_dont_duplicate = True

# When importing from bibtex, check that categories are according to
# the bibtex standard.
# If False, then all categories allowed.
use_standard_categories = True

# When importing a file, do not validate and do not process duplicates
simple_import = False

# Common typos
typos_common = {"\\a\\'": "\\'",
                "": " ",
                "{\\r A}": "{\\AA}",
                "{\\r a}": "{\\aa}"}

# Typos in author strings
typos_author = {"&": None,
                "(": None,
                ")": None,
                ",": None}

# Typos in editor strings
typos_editor = typos_author

# Typos in key strings
typos_key = {"\_": ""}

# Collect typos
typos = {"common": typos_common,
         "author": typos_author,
         "editor": typos_editor,
         "key":    typos_key}

institutions = ("Carleton University",
                "Finite Element Center",
                "InterMedia, University of Oslo",
                "Norwegian University of Science and Technology",
                "Numerical Objects A.S.",
                "University of Castilla-La Mancha",
                "Simula Research Laboratory")

schools = ("Department of Informatics, University of Oslo",
           "Faculty of Mathematics and Natural Sciences, University of Oslo")

publishers = ("Birkh{\\\"a}user",
              "Cambridge University Press",
              "Chapman and Hall",
              "Computers in Cardiology",
              "Elsevier Science",
              "EuroPACS",
              "European Association of Geoscientists \\& Engineers",
              "European Community on Computational Methods in Applied Sciences",
              "Informing Science Press",
              "John von Neumann Institute for Computing",
              "Kluwer Academic Publishers",
              "Literat{\\\"u}r Yayincilik Ltd.",
              "MGNet",
              "Nationellt centrum f{\\\"o}r matematikutbildning, NCM",
              "North Holland",
              "Nova Science Publishers",
              "SIAM",
              "SPIE",
              "Springer",
              "Swansea",
              "Tapir Academic Press",
              "Taylor \\& Francis Books Ltd",
              "Wiley Press")

# Words that should not be capitalized
lowercase = ["a", "an", "and", "at", "for", "in", "of", "on", "the", "to", "by"]

# Words that should be capitalized
uppercase = {
    "python": "{P}ython",
    "cython": "{C}ython",
    "fortran": "{FORTRAN}",
    "c++":    "{C}++",
    "matlab": "{MATLAB}",
    "xml": "{XML}",
    "java": "{Java}",
    "perl": "{P}erl",
    "ruby": "{R}uby}",
    "diffpack": "{D}iffpack",
    "dolfin": "{DOLFIN}",
    "swig": "{SWIG}",
    "instant": "{I}nstant",
    "oo": "{OO}",
    "planck": "{Planck}",
    "fouirer": "{F}ourier",
    "fokker-planck": "{Fokker-Planck}",
    "navier-stokes": "{Navier-Stokes}",
    "fenics": "{FEniCS}",
    "newton": "{N}ewton",
    "markov":"{Markov}",
    "boltzmann": "{B}oltzmann",
    "lattice-boltzmann": "{Lattice-Boltzmann}",
    "lagrange":"{Lagrange}",
    "laplacian":"{Laplacian}",
    "laplace": "{L}aplace",
    "poisson": "{P}oisson",
    "poisson's": "{P}oisson's",
    "ode": "{ODE}",
    "pde": "{PDE}",
    "fdm": "{FDM}",
    "fvm": "{FVM}",
    "fem": "{FEM}",
    "fsi": "{FSI}",
    " fe ": " {FE} ",
    " fd ": " {FD} ",
    "pdes": "{PDE}s",
    "odes": "{ODE}s",
    "ode's": "{ODE}'s",
    "pde's": "{PDE}'s",
    "infiniband": "{I}nfini{B}and",
    "ethernet": "{E}thernet",
    "mapreduce": "{M}ap{R}educe",
    "tcp": "{TCP}",
    "cpu": "{CPU}",
    "cpus": "{CPU}s",
    "gpu": "{GPU}",
    "gpus": "{GPU}s",
    "mpi": "{MPI}",
    "openmp": "{O}pen{MP}",
    "cuda": "{CUDA}",
    "cfd": "{CFD}",
    "hpc": "{HPC}",
    "mpeg":"{MPEG}",
    }

journals = [("none", "none", "xxxx-xxxx"),
            ("ACM Trans. Math. Software", "ACM Transactions on Mathematical Software", "0098-3500"),
            ("ACM Comput. Surv.", "ACM Computing Surveys", "0360-0300"),
            ("ACM SIGSOFT Software Engineering Notes", "ACM SIGSOFT Software Engineering Notes", "01635848"),
            ("ACM Trans. Multimed. Comput. Comm. Appl.", "ACM Transactions on Multimedia Computing, Communications, and Applications", "1551-6857"),
            ("ACM Trans. Software Eng. Meth.", "ACM Transactions on Software Engineering and Methodology", "1049-331X"),
            ("Adv. Comput. Math.", "Advances in Computational Mathematics", "1019-7168"),
            ("Adv. Water Resour.", "Advances in Water Resources", "0309-1708"),
            ("Ann. Biomed. Eng.", "Annals of Biomedical Engineering", "0090-6964"),
            ("Appl. Cognit. Psychol.", "Applied Cognitive Psychology", "0888-4080"),
            ("Appl. Math. Comput.", "Applied Mathematics and Computation", "0096-3003"),
            ("Appl. Math. Finance", "Applied Mathematical Finance", "1350-486X"),
            ("Appl. Math. Model.", "Applied Mathematical Modelling", "0307-904X"),
            ("Appl. Mech. Eng.", "Applied Mechanics and Engineering", "1425-1655"),
            ("Arch. Comput. Methods Eng.", "Archives of Computational Methods in Engineering", "1134-3060"),
            ("Behaviour \\& Information Technology", "Behaviour \\& Information Technology", "0144-929X"),
            ("Biophys. J.", "Biophysical Journal", "0006-3495"),
            ("BIT", "BIT Numerical Mathematics", "0006-3835"),
            ("Camput-Wide Information Systems", "Campus-Wide Information Systems", "1065-0741"),
            ("Comput. Biol. Med.", "Computers in Biology and Medicine", "0010-4825"),
            ("Comput. Comm.", "Computer Communications", "0140-3664"),
            ("Comput. Geosci.", "Computational Geosciences", "1420-0597"),
            ("Comput. Phys.", "Communications in Computational Physics", "1814-2406"),
            ("Comput. Math. Appl.", "Computers \\& Mathematics with Applications", "0898-1221"),
            ("Comput. Mech.", "Computational Mechanics. Solids, Fluids, Engineered Material, Aging Infrastructure, Molecular Dynamics, Heat Transfer, Manufacturing Processes, Optimization, Fracture \& Integrity", "0178-7675"),
            ("Comput. Methods Appl. Mech. Engrg", "Computer Methods in Applied Mechanics and Engineering", "0045-7825"),
            ("Comput. Meth. Biomech. Biomed. Eng.", "Computer Methods in Biomechanics and Biomedical Engineering", "1025-5842"),
            ("Comput. Sci. Eng.", "Computing in Science \\& Engineering", "1521-9615"),
            ("Comput. Vis. Sci.", "Computing and Visualization in Science", "1432-9360"),
            ("Continent. Shelf Res.", "Continental Shelf Research", "0278-4343"),
            ("Empir. Software Eng.", "Empirical Software Engineering", "1382-3256"),
            ("Eng. Anal. Bound. Elem.", "Engineering Analysis with Boundary Elements", "0955-7997"),
            ("Formal Aspect. Comput.", "Formal Aspects of Computing", "0934-5043"),
            ("Future Generat. Comput. Syst.", "Future Generation Computer Systems", "0167-739X"),
            ("Global J. Pure Appl. Math.", "Global Journal of Pure and Applied Mathematics", "0973-1768"),
            ("IEEE/ACM Transactions on Networking", "IEEE/ACM Transactions on Networking", "1063-6692"),
            ("IEEE Comm. Lett.", "IEEE Communications Letters", "1089-7798"),
            ("IEEE Comm. Mag.", "IEEE Communications Magazine", "0163-6804"),
            ("IEEE Comput. Appl. Power Mag.", "IEEE Computer Applications in Power Magazine", "0895-0156"),
            ("IEEE Comput. Architect. Lett.", "IEEE Computer Architecture Letters", "1556-6056"),
            ("IEEE Control Syst. Mag.", "IEEE Control Systems Magazine", "1066-033X"),
            ("IEEE Distr. Syst. Online", "IEEE Distributed Systems Online", "1541-4922"),
            ("IEEE Micro Magazine", "IEEE Micro Magazine", "0272-1732"),
            ("IEEE Netw. Mag. Global Inform. Exchange", "IEEE Network: The Magazine of Global Information Exchange", "0890-8044"),
            ("IEEE Software Mag.", "IEEE Software Magazine", "0740-7459"),
            ("IEEE Trans. Biomed. Eng.", "IEEE Transactions on Biomedical Engineering", "0018-9294"),
            ("IEEE Trans. Comput.", "IEEE Transactions on Computers", "0018-9340"),
            ("IEEE Transactions on Industrial Informatics", "IEEE Transactions on Industrial Informatics", "1551-3203"),
            ("IEEE Trans. Parallel Distr. Syst.", "IEEE Transactions on Parallel and Distributed Systems", "1045-9219"),
            ("IEEE Trans. Software Eng.", "IEEE Transactions on Software Engineering", "0098-5589"),
            ("IEEE Trans. Wireless Comm.", "IEEE Transactions on Wireless Communications", "1536-1276"),
            ("IET Communications", "IET Communications", "1751-8628"),
            ("IMA J. Appl. Math.", "IMA Journal of Applied Mathematics", "0272-4960"),
            ("IMA J. Numer. Anal.", "IMA Journal of Numerical Analysis", "0272-4979"),
            ("Inform. Process. Lett.", "Information Processing Letters", "0020-0190"),
            ("Inform. Software Tech.", "Information and Software Technology", "0950-5849"),
            ("ISA Transactions", "ISA Transactions", "0019-0578"),
            ("Appl. Mech. Eng.", "International Journal of Applied Mechanics and Engineering", "1425-1655"),
            ("J. Comput. Methods Eng. Sci. Mech.", "International Journal for Computational Methods in Engineering Science and Mechanics", "1550-2287"),
            ("International Journal of Autonomous and Adaptive Communications Systems", "International Journal of Autonomous and Adaptive Communications Systems", "1754-8632"),
            ("International Journal of Bioelectromagnetism", "International Journal of Bioelectromagnetism", "1456-7857"),
            ("Int. J. Comput. Eng. Sci.", "International Journal of Computational Engineering Science", "1465-8763"),
            ("IJCSE", "International Journal of Computational Science and Engineering", "1742-7185"),
            ("Int. J. Comput. Math.", "International Journal of Computer Mathematics", "0020-7160"),
            ("Int. J. Forecast", "International Journal of Forecasting", "0169-2070"),
            ("Int. J. Fluid Mech. Res.", "International Journal of Fluid Mechanics Research", "1064-2277"),
            ("Int. J. Numer. Anal. Model.", "International Journal of Numerical Analysis and Modeling", "1705-5105"),
            ("Int. J. Nonlinear Sci. Numer. Simul.", "International Journal of Nonlinear Sciences and Numerical Simulation", "1565-1339"),
            ("Int. J. Nonlinear Model. Sci. Eng.", "International Journal of Nonlinear Modelling in Science and Engineering", "1472-085X"),
            ("Int. J. Numer. Meth. Eng.", "International Journal for Numerical Methods in Engineering", "0029-5981"),
            ("Int. J. Numer. Meth. Fluid.", "International Journal for Numerical Methods in Fluids", "0271-2091"),
            ("Int. J. Proj. Manag.", "International Journal of Project Management", "0263-7863"),
            ("International Journal of Pure and Applied Mathematics", "International Journal of Pure and Applied Mathematics", "1311-8080"),
            ("Int. J. Software Eng. Knowl. Eng.", "International Journal of Software Engineering and Knowledge Engineering", "0218-1940"),
            ("J. Comput. Acoust", "Journal of Computational Acoustics", "0218-396X"),
            ("J. Comput. Appl. Math.", "Journal of Computational and Applied Mathematics", "0377-0427"),
            ("J. Comput. Finance", "Journal of Computational Finance", "1460-1559"),
            ("J. Comput. Neurosci.", "Journal of Computational Neuroscience", "0929-5313"),
            ("J. Comput. Phys.", "Journal of Computational Physics", "0021-9991"),
            ("Journal d'Analyse Mathematique", "Journal d'Analyse Mathematique", "0021-7670"),
            ("J. Geodyn.", "Journal of Geodynamics", "0264-3707"),
            ("J. Geophys. Res. B", "Journal of Geophysical Research (JGR)-B", "0196-6936"),
            ("Journal of Medical Ultrasonics", "Journal of Medical Ultrasonics", "1346-4523"),
            ("J. Netw. Comput. Appl.", "Journal of Network and Computer Applications", "1084-8045"),
            ("J. Numer. Math.", "Journal of Numerical Mathematics", "1570-2820"),
            ("J. Object Tech.", "Journal of Object Technology", "1660-1769"),
            ("J. Sci. Comput.", "Journal of Scientific Computing", "0885-7474"),
            ("J. Software Mainten. Evol. Res. Pract.", "Journal of Software Maintenance and Evolution: Research and Practice", "1532-060X"),
            ("J. Stat. Software", "Journal of Statistical Software", "1548-7660"),
            ("J. Syst. Architect.", "Journal of Systems Architecture", "1383-7621"),
            ("J. Syst. Software", "Journal of Systems and Software", "0164-1212"),
            ("Math. Biosci.", "Mathematical Biosciences", "0025-5564"),
            ("Math. Comp.", "Mathematics of Computation", "0025-5718"),
            ("Math. Comput. Simulat.", "Mathematics and Computers in Simulation", "0378-4754"),
            ("Math. Geol.", "Mathematical Geology", "0882-8121"),
            ("Metheoritics Planet. Sci.", "Metheoritics \\& Planetary Science", "1086-9379"),
            ("Mobile Network. Appl.", "Mobile Networks and Applications", "1383-469X"),
            ("Model. Identif. Control", "Modeling, Identification and Control. A Norwegian Research Bulletin", "0332-7353"),
            ("Multi Agent and Grid Systems", "Multi Agent and Grid Systems", "1574-1702"),
            ("Nord. J. Comput.", "Nordic Journal of Computing", "1236-6064"),
            ("Norwegian Journal of Geography/ Norsk Geografisk Tidsskrift", "Norwegian Journal of Geography/ Norsk Geografisk Tidsskrift", "0029-1951"),
            ("Numer. Linear Algebra Appl.", "Numerical Linear Algebra with Applications", "1070-5325"),
            ("Numer. Methods Partial Differential Equations", "Numerical Methods for Partial Differential Equations. An International Journal", "0749-159X"),
            ("Numer. Math.", "Numerische Mathematik", "0029-599X"),
            ("Otic. Comm.", "Optics Communications", "0030-4018"),
            ("Perform. Eval.", "Performance Evaluation", "0166-5316"),
            ("Personal and Ubiquitous Computing", "Personal and Ubiquitous Computing", "1617-4909"),
            ("Phys. Earth Planet. In.", "Physics of the Earth and Planetary Interiors", "0031-9201"),
            ("Phys. Rev. B Condens. Matter", "Physical Review B: Condensed Matter and Materials Physics", "1098-0121"),
            ("Proc. IEEE Comput. Soc. Bioinformatics Conf. IEEE Comput. Soc. Bioinformatic", "Proceedings / IEEE Computer Society Bioinformatics Conference. IEEE Computer Society Bioinformatics Conference", "1555-3930"),
            ("Research Letters in Communications", "Research Letters in Communications", "1687-6741"),
            ("Scand. J. Inform. Syst.", "Scandinavian Journal of Information Systems", "0905-0167"),
            ("Sci. Program.", "Scientific Programming", "1058-9244"),
            ("SIAM J. Numer. Anal.", "SIAM Journal on Numerical Analysis", "0036-1429"),
            ("SIAM J. Sci. Comput.", "SIAM Journal on Scientific Computing", "1064-8275"),
            ("Software Process Improv. Pract.", "Software Process: Improvement and Practice", "1077-4866"),
            ("Software Syst. Model.", "Software and Systems Modeling", "1619-1366"),
            ("Stroke", "Stroke", "0039-2499"),
            ("Transactions on Machine Learning and Data Mining", "Transactions on Machine Learning and Data Mining", "1865-6781"),
            ("Transp. Porous Media", "Transport in Porous Media", "0169-3913"),
            ("Wireless Pers. Comm.", "Wireless Personal Communications", "0929-6212")]

# Categories
categories = ("articles",
              "books",
              "edited",
              "chapters",
              "refproceedings",
              "proceedings",
              "reports",
              "manuals",
              "theses",
              "courses",
              "talks",
              "posters",
              "publicoutreach",
              "preprint",
              "misc")

# Headings for categories
category_headings = {"articles":       "Articles in International Journals",
                     "books":          "Books",
                     "edited":         "Edited Books",
                     "chapters":       "Chapters in Books",
                     "refproceedings": "Refereed Proceedings",
                     "proceedings":    "Conference Proceedings",
                     "reports":        "Technical Reports",
                     "manuals":        "Manuals",
                     "theses":         "Theses",
                     "courses":        "Courses",
                     "talks":          "Talks",
                     "posters":        "Posters",
                     "publicoutreach": "Public Outreach",
                     "preprint":       "Preprints",
                     "misc":           "Other Publications"}

# Labels for categories
category_labels = {"articles":       "J",
                   "books":          "B",
                   "edited":         "E",
                   "chapters":       "C",
                   "refproceedings": "P",
                   "proceedings":    "Pc",
                   "reports":        "R",
                   "manuals":        "M",
                   "theses":         "T",
                   "courses":        "Co",
                   "talks":          "Ta",
                   "posters":        "Po",
                   "publicoutreach": "Or",
                   "preprint":       "Pr",
                   "misc":           "Mi"}

# Attributes for categories (tuple means at least one of listed attributes required)
category_attributes = {"articles":       ("author", "title", "journal", "year", "status"),
                       "books":          ("author", "title", "publisher", "year", "status"),
                       "edited":         ("author", "title", "publisher", "year", "status"),
                       "chapters":       ("author", "title", "editor", "publisher", "year", "status"),
                       "refproceedings": ("author", "title", "booktitle", "year", "status"),
                       "proceedings":    ("author", "title", "booktitle", "year", "status"),
                       "reports":        ("author", "title", "institution", "year", "status"),
                       "manuals":        ("author", "title", "status"),
                       "theses":         ("author", "title", "school", "year", "thesistype", "status"),
                       "courses":        ("author", "title", "code", "institution", "year", "status"),
                       "talks":          ("author", "title", "meeting", "year", "status"),
                       "posters":        ("author", "title", "meeting", "year", "status"),
                       "publicoutreach": ("author", "title", "meeting", "year", "status"),
                       "preprint":       ("author", "title", "year", "status"),
                       "misc":           ("title", "status")}

# Venues for categories (will be matched against a list of allowed values)
category_venues = {"articles":       "journal",
                   "books":          "publisher",
                   "edited":         "publisher",
                   "chapters":       "publisher",
                   "refproceedings": None,
                   "proceedings":    None,
                   "reports":        "institution",
                   "manuals":        None,
                   "theses":         "school",
                   "courses":        "institution",
                   "talks":          "meeting",
                   "posters":        "meeting",
                   "publicoutreach": "meeting",
                   "preprint":       None,
                   "misc":           None}

# List of ordered attributes (so we rewrite pub files in a fixed order)
ordered_attributes = ("title",
                      "key",
                      "author", "editor",
                      "year",
                      "date",
                      "journal", "booktitle", "institution", "meeting",
                      "publisher",
                      "volume",
                      "number",
                      "chapter",
                      "pages",
                      "num_pages",
                      "doi",
                      "arxiv",
                      "pdf",
                      "url",
                      "status",
                      "duplicate",
                      "allowed_duplicates",
                      "tags",
                      "private",
                      "fixme")

# Entry types (BibTeX)
entrytypes = ("article",
              "book",
              "booklet",
              "conference",
              "inbook",
              "incollection",
              "inproceedings",
              "manual",
              "mastersthesis",
              "misc",
              "phdthesis",
              "proceedings",
              "techreport",
              "preprint",
              "unpublished")

# Attributes for entry types (tuple means at least one of listed attributes required)
entrytype_attributes = {"article":      ("author", "title", "journal", "year"),
                        "book":         (("author", "editor"), "title", "publisher", "year"),
                        "booklet":      ("title",),
                        "conference":   ("author", "title", "booktitle", "year"),
                        "inbook":       (("author", "editor"), "title", ("chapter", "pages"), "publisher", "year"),
                        "incollection": ("author", "title", "booktitle", "publisher", "year"),
                        "inproceedings":("author", "title", "booktitle", "year"),
                        "manual":       ("title",),
                        "mastersthesis": ("author", "title", "school", "year"),
                        "misc":         (),
                        "phdthesis":    ("author", "title", "school", "year"),
                        "proceedings":  ("title", "year"),
                        "techreport":   ("author", "title", "institution", "year"),
                        "preprint":     ("author", "title"),
                        "unpublished":  ("author", "title", "note")}

# Mapping from entry type to category
entrytype2category = {"article":          "articles",
                      "book":             None,            # special case: books or edited
                      "book proceedings": "edited",
                      "inbook":           "chapters",
                      "inproceedings":    "proceedings",
                      "conference":       "proceedings",
                      "techreport":       "reports",
                      "manual":           "manuals",
                      "preprint":         "preprint",
                      "phdthesis":        None,            # special case: theses
                      "mastersthesis":    None,            # special case: theses
                      "misc":             None}            # special case: misc, talks, or courses

# Mapping from category to entry type
category2entrytype = {"articles":       "article",
                      "books":          "book",
                      "edited":         "book",
                      "chapters":       "inbook",
                      "refproceedings": "inproceedings",
                      "proceedings":    "inproceedings",
                      "reports":        "techreport",
                      "manuals":        "manual",
                      "theses":         None,
                      "courses":        "misc",
                      "talks":          "misc",
                      "preprint":       "preprint",
                      "misc":           "misc"}

# Thesis type strings
thesistype_strings = {"phd":     "Ph.D. Thesis",
                      "msc":     "M.Sc. Thesis",
                      "lic":     "Lic. Thesis",
                      "diploma": "Dipl. Thesis"}
