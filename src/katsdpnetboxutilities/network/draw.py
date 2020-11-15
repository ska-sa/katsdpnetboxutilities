#!/usr/bin/env python3

import sys
import logging
import json
from pathlib import Path

import configargparse

from katsdpnetboxutilities.connect import NetboxConnection
from katsdpnetboxutilities.network.utils import make_dot_file_from_path


def parse_args():
    """Parse command line, config file and environmental variables.

    See configargparse for more detail.
    """
    p = configargparse.ArgParser(default_config_files=["~/.config/sarao/netbox"])
    p.add("-c", "--config", is_config_file=True, help="config file")
    p.add(
        "-w",
        "--working-path",
        required=True,
        help=(
            "Path where the definitian files are located and "
            "output files will be stored"
        ),
    )
    p.add("-n", "--name", help="Graph name")
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
    config, unknown = p.parse_known_args()
    config = vars(config)
    config["working_path"] = Path(config["working_path"])

    if not config["working_path"].exists() or not config["working_path"].is_dir():
        raise ValueError(
            "The working path do not exists"
        )  # A custom exception would be nice

    if not config.get("name"):
        config["name"] = config["working_path"].name

    logger = logging.getLogger()
    if config["debug"]:
        logger.setLevel(logging.DEBUG)
    elif config["verbose"]:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)

    config["output_path"] = config["working_path"]
    logging.debug(p.format_values())
    logging.debug("Config: %s", config)
    return config


class QueryDefinitian:
    def __init__(self, config):
        self.config = config
        self.workpath = config["working_path"]
        self.query = {"sites": {}, "racks": {}, "devices": {}, "tenants": {}}

    def read(self):
        """Read in the definitian files."""
        for name in self.query.keys():
            include, exclude = self._read_definitian(name)
            self.query[name]["include"] = include
            self.query[name]["exclude"] = exclude
        # TODO: Query each rack and get all the devices.
        # TODO: Query each site and get all the devices.

    def include_device(self, obj: dict = None, name: str = None, device_id: int = None):
        if obj:
            logging.info("Add device %s", obj.get("name", obj["id"]))
            self.include_device(device_id=obj["id"])
        elif name:
            self.query["devices"]["include"].add(name)
        elif device_id:
            self.query["devices"]["include"].add("id:{}".format(device_id))
        else:
            raise ValueError("No name or device_id given")

    def exclude_device(self, obj: dict = None, name: str = None, device_id: int = None):
        if obj:
            logging.info("Add device %s", obj.get("name", obj["id"]))
            self.include_device(device_id=obj["id"])
        elif name:
            self.query["devices"]["exclude"].add(name)
        elif device_id:
            self.query["devices"]["exclude"].add("id:{}".format(device_id))
        else:
            raise ValueError("No name or device_id given")

    def devices(self):
        # Check each device to make sure it is not in the exclude list
        return self.query["devices"]["include"]

    def _read_definitian(self, name):
        plfile = Path(self.workpath) / name
        include_items = set()
        exclude_items = set()
        if plfile.exists():
            with plfile.open() as openfile:
                for line in openfile.readlines():
                    if line.startswith("#"):
                        continue
                    elif line.startswith("-"):
                        item = line.strip("-").strip()
                        logging.error("exclude %s %s - not implemented!", name, item)
                        exclude_items.add(item)
                    elif line.startswith("+"):
                        item = line.strip("+").strip()
                        logging.info("include %s %s", name, item)
                        include_items.add(item)
                    else:
                        logging.warning(
                            "In %s the line '%s' will be ignored", plfile, line
                        )
        return include_items, exclude_items

    def save_connections(self, interfaces):
        for result in interfaces.get("results", []):
            devicea = "{}:{}".format(
                result["interface_a"]["device"]["name"], result["interface_a"]["name"]
            )
            deviceb = "{}:{}".format(
                result["interface_b"]["device"]["name"], result["interface_b"]["name"]
            )
            name = "+".join(sorted([devicea, deviceb]))
            filename = "connection+{}".format(name).replace("/", "_")
            plfile = Path(self.workpath) / filename
            with plfile.open("w+") as openfile:
                json.dump(result, openfile)


def main():
    try:
        config = parse_args()
    except Exception as error:
        logging.error(error)
        sys.exit(1)
    make_dot_file_from_path(config)


if __name__ == "__main__":
    main()
