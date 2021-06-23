#!/usr/bin/env python3

import sys
import yaml

def make_header(NAME):
    header_file = ["usepackage{fancyhdr}","pagestyle{fancy}", "fancyhf{}"]
    header_file.append("rhead{\\textbf{%s}}" % NAME)
    with open("/reports/header.tex", "w+") as f:
        for txt in header_file:
            f.write("\\" + txt + "\n")
        f.close()

def make_pandoc_yaml(NAME):
    config_dict = {
      "standalone": True,
      "self-contained": True,
      "variables": {
        "documentclass": "book",
        "classoption":
        [ "oneside",
        "draft"]

      },
      "metadata": {
        "author": [
          "SARAO SDP"
        ],
        "title": [
          f"SDP System: {NAME}"
        ],
        "fontfamily":["courier"]
      },
      "include-before-body": [],
      "include-after-body": [],
      "include-in-header":[],
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
      "dpi": 300,
      "extract-media": "mediadir",
      "table-of-contents": True,
      "toc-depth": 4,
      "number-sections": True,
      "shift-heading-level-by": 0,
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
    yaml.dump(config_dict, open("/reports/pandoc.yaml", "w"), default_flow_style=False)
