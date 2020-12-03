#!/usr/bin/env python3

import logging
import json
from pathlib import Path

import configargparse

from katsdpnetboxutilities.connect import NetboxConnection


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
        "-w",
        "--working-path",
        required=True,
        help=(
            "Path where the output files will be stored"
        ),
    )
    p.add("-v", "--verbose", help="Verbose", action="store_true")
    p.add("-d", "--debug", help="Debug", action="store_true")
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

def add_host_to_domain(config, domain, host):
    pfile = Path(config['working_path']) / domain

    with pfile.open("a+") as fh:
        fh.write(json.dumps(host))
        fh.write("\n")

def main():
    config = parse_args()
    netbox = NetboxConnection(config)
    for addr in netbox.ipaddresses():
        if addr.get('dns_name'):
            dns_name = addr['dns_name']
            hostname, domain = dns_name.split(".", 1)
            add_host_to_domain(config, domain, addr)
            print(hostname, domain, addr)


if __name__ == "__main__":
    main()
