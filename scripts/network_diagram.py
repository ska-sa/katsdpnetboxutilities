#!/usr/bin/env python3

import logging

import configargparse

from katsdpnetboxutilities.connect import query_netbox
from katsdpnetboxutilities.network_diagram import make_dot_file


def parse_args():
    """Parse command line, config file and environmental variables.

    See configargparse for more detail.
    """
    p = configargparse.ArgParser(default_config_files=["~/.config/sarao/netbox"])
    p.add("-c", "--config", is_config_file=True, help="config file")
    p.add("--token", help="Netbox connection token")
    p.add("--url", help="Netbox server URL")
    p.add("--cache-path", help="Directory to store temporary results")
    p.add("-o", required=True, help="Outfile")
    p.add("-v", "--verbose", help="Verbose", action="store_true")
    p.add("-d", "--debug", help="Debug", action="store_true")
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


if __name__ == "__main__":
    config = parse_args()
    path = "/api/dcim/interface-connections"
    query = {}
    print(config["search"])
    for query_item in config["search"]:
        key, value = query_item.split("=", 1)
        query[key] = value
    data = query_netbox(
        config["url"], config["token"], path, query, config["cache_path"]
    )
    make_dot_file(config["o"], data.get("results"))