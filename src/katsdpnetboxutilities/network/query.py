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
            "Path where the definitian files are located and "
            "output files will be stored"
        ),
    )
    # p.add("-n", "--name", required=True, help="Graph name")
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
    # p.add("search", nargs="+", help="Netbox search filter")
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
    config = parse_args()
    qdef = QueryDefinitian(config)
    netbox = NetboxConnection(config)
    qdef.read()

    for def_type, definition in qdef.query.items():
        if def_type == 'devices':
            continue
        for item in definition['include']:
            for device in netbox.devices({def_type.rstrip('s'): item}):
                qdef.include_device(obj=device)

        for item in definition['exclude']:
            for device in netbox.devices({def_type.rstrip('s'): item}):
                qdef.exclude_device(obj=device)

    for device in qdef.devices():
        print("query device=", device)
        data = netbox.device_interfaces(device)
        qdef.save_connections(data)


if __name__ == "__main__":
    main()
