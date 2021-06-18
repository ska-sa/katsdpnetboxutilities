#!/usr/bin/env python3

import sys
import yaml

NAME = sys.argv[1]

header_file = ["usepackage{fancyhdr}", "pagestyle{fancy}", "fancyhf{}"]


header_file.append("rhead{\\textbf{%s}}" % NAME)

with open("header.tex", "w+") as f:
    for txt in header_file:
        f.write("\\" + txt + "\n")

    f.close()


config_dict = {
  "standalone": True,
  "self-contained": True,
  "variables": {
    "documentclass": "book",
    "classoption": [
      "twosides",
      "draft"
    ]
  },
  "metadata": {
    "author": [
      "SARAO SDP"
    ],
    "title": [
      f"SDP System: {NAME}"
    ],
    "fontfamily":["Courier"]
  },
  "include-before-body": [],
  "include-after-body": [],
  "include-in-header":
    "header.tex"
  ,
  "resource-path": [
    '\".\"'
  ],
  "citeproc": True,
  "file-scope": False,
  "verbosity": "INFO",
  "log-file": "log.json",
  "cite-method": "citeproc",
  "top-level-division": "chapter",
  "abbreviations": None,
  "pdf-engine": "pdflatex",
  "pdf-engine-opts": [
    "-shell-escape"
  ],
  "wrap": "auto",
  "columns": 78,
  "dpi": 72,
  "extract-media": "mediadir",
  "table-of-contents": True,
  "toc-depth": 4,
  "number-sections": True,
  "shift-heading-level-by": 1,
  "section-divs": True,
  "identifier-prefix": "foo",
  "title-prefix": "",
  "strip-empty-paragraphs": True,
  "eol": "lf",
  "strip-comments": False,
  "indented-code-classes": [],
  "ascii": False,
  "default-image-extension": ".jpg",
  "highlight-style": "pygments",
  "listings": False,
  "html-math-method": {
    "method": "mathjax",
    "url": '\"https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js\"'
  },
  "email-obfuscation": "javascript",
  "tab-stop": 8,
  "preserve-tabs": True,
  "incremental": False,
  "slide-level": 2,
  "reference-links": True,
  "reference-location": "block",
  "markdown-headings": "setext",
  "track-changes": "accept",
  "html-q-tags": False,
  "ipynb-output": "best",
  "request-headers": [
    [
      "User-Agent",
      "Mozilla/5.0"
    ]
  ],
  "fail-if-warnings": False,
  "dump-args": False,
  "ignore-args": False,
  "trace": False
}
yaml.dump(config_dict, open("pandoc.yaml", "w"), default_flow_style=False)
