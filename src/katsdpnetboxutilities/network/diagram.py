#!/usr/bin/env python3

import logging

import configargparse

from katsdpnetboxutilities.connect import query_netbox
from katsdpnetboxutilities.network.utils import make_dot_file


def parse_args():
    """Parse command line, config file and environmental variables.

    See configargparse for more detail.
    """
    p = configargparse.ArgParser(default_config_files=["~/.config/sarao/netbox"])
    p.add("-c", "--config", is_config_file=True, help="config file")
    p.add("--token", help="Netbox connection token")
    p.add("--url", help="Netbox server URL")
    p.add("--cache-path", help="Directory to store temporary results")
    p.add("--cache-age", help="How old cache objects can get (minutes)", default=600)
    p.add(
        "-o",
        "--output-path",
        required=True,
        help="Path where the output files will be stored",
    )
    p.add("-n", "--name", required=True, help="Graph name")
    p.add("-v", "--verbose", help="Verbose", action="store_true")
    p.add("-d", "--debug", help="Debug", action="store_true")
    p.add("-l", "--live", help="Live view, display the graph", action="store_true")
    p.add(
        "--subgraph",
        help="Make nodes subgraphs, do not work with all engines",
        action="store_true",
    )
    p.add(
        "--horizontal",
        help="Attempt to produce a horizontal layout if possible",
        action="store_true",
    )
    p.add(
        "-e",
        "--engine",
        help="Graph layout engine to use",
        default="dot",
        choices=["dot", "neato", "sfdp", "circo"],
    )
    p.add("-f", "--format", help="Output format", default="pdf", choices=["pdf", "png"])
    p.add("search", nargs="+", help="Netbox search filter")
    config = vars(p.parse_args())

    logger = logging.getLogger()
    if config["debug"]:
        logger.setLevel(logging.DEBUG)
    elif config["verbose"]:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)

    logging.debug(p.format_values())
    logging.debug("Config: %s", config)
    return config


def main():
    config = parse_args()
    path = "/api/dcim/interface-connections"
    query = {}
    for query_item in config["search"]:
        key, value = query_item.split("=", 1)
        query[key] = value
    data = query_netbox(config, path, query)
    make_dot_file(config, data.get("results"))
