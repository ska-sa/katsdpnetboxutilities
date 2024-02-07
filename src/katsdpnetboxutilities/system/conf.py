project = "sdp-systems"
copyright = "2020, SDP"
author = "SDP"
version = ""
release = ""
templates_path = ["_templates"]
source_suffix = [".rst", ".md"]
master_doc = "index"
html_theme = "alabaster"
html_static_path = ["_static"]
htmlhelp_basename = "sdp-systems"
latex_elements = {
    "papersize": "a4paper",
    "preamble": "\\usepackage[nodayofweek]{datetime}",
    "extraclassoptions": "openany,oneside",
}
latex_documents = [
    (
        master_doc,
        "sdp-system.tex",
        "epyc01 System",
        author,
        "howto",
    )
]
man_pages = [(master_doc, "sdp-system", "sdp-system Documentation", [author], 1)]
texinfo_documents = [
    (
        master_doc,
        "sdp-system",
        "sdp-system Documentation",
        author,
        "sdp-system",
        "One line description of project.",
        "Miscellaneous",
    ),
]
extensions = [
    "sphinx.ext.graphviz",
    "sphinx.ext.ifconfig",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx-prompt",
    "sphinxcontrib.actdiag",
    "sphinxcontrib.blockdiag",
    "sphinxcontrib.excel_table",
    "sphinxcontrib.nwdiag",
    "sphinxcontrib.packetdiag",
    "sphinxcontrib.plantuml",
    "sphinxcontrib.rackdiag",
    "sphinxcontrib.seqdiag",
]
html_theme = "sphinx_rtd_theme"
todo_include_todos = True
source_suffix = [".rst", ".md"]
from recommonmark.parser import CommonMarkParser

source_parsers = {
    ".md": CommonMarkParser,
}
