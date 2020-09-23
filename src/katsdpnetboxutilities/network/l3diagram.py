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
    path = "/api/ipam/prefixes/"
    query = {}
    for query_item in config["search"]:
        key, value = query_item.split("=", 1)
        query[key] = value
    data = query_netbox(config, path, query)
    print(data)
    # make_dot_file(config, data.get("results"))
