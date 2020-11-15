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


class QueryDefinitian:
    def __init__(self, config, netbox):
        self.config = config
        self._netbox = netbox
        self.workpath = config["working_path"]
        self.query = {
            "sites": {},
            "racks": {},
            "devices": {},
            "tenants": {},
            "tags": {}
        }
        # The device_ids is the final include/exclude set for the devices we will query for connections.
        self._device_ids = {"include": set(), "exclude": set()}

    def read(self):
        """Read in the definitian files."""
        for name in self.query.keys():
            include, exclude = self._read_definitian(name)
            self.query[name]["include"] = include
            self.query[name]["exclude"] = exclude

    def filter(self):
        """Go through the include and exclude sets and create include & exclude set of device_id."""
        logging.debug("Query %s", self.query)
        for def_type in ["include", "exclude"]:
            for device in self.query["devices"][def_type]:
                if device.startswith("id:"):
                    device_id = int(device.split(":")[1])
                    self._device_ids[def_type].add(device_id)
                else:
                    for device_id in self._netbox.lookup_device_ids(device):
                        self._device_ids[def_type].add(device_id)
        logging.debug("Devices IDs after filter: %s", self._device_ids)

    def include_device(self, obj: dict = None, name: str = None, device_id: int = None):
        if obj:
            logging.info("Add device %s", obj.get("name", obj["id"]))
            self.include_device(device_id=obj["id"])
        elif name:
            if name not in self.query["devices"]["exclude"]:
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
        """The devices that are in the include set and not in the exclude set."""
        return self._device_ids["include"].difference(self._device_ids["exclude"])

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
                        logging.warning("exclude %s %s", name, item)
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
            if result["interface_a"]["device"]["id"] in self._device_ids["exclude"]:
                logging.info(
                    "ignoring link to %s device in exclude list",
                    result["interface_a"]["device"]["name"],
                )
                continue
            elif result["interface_b"]["device"]["id"] in self._device_ids["exclude"]:
                logging.info(
                    "ignoring link to %s device in exclude list",
                    result["interface_a"]["device"]["name"],
                )
                continue
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
    netbox = NetboxConnection(config)
    qdef = QueryDefinitian(config, netbox)
    qdef.read()

    for def_type, definition in qdef.query.items():
        if def_type == "devices":
            continue
        for item in definition["exclude"]:
            for device in netbox.devices(key=def_type.rstrip("s"), value=item):
                qdef.exclude_device(obj=device)

        for item in definition["include"]:
            for device in netbox.devices(key=def_type.rstrip("s"), value=item):
                qdef.include_device(obj=device)

    qdef.filter()

    for device in qdef.devices():
        logging.info("query device:%s", device)
        data = netbox.device_interfaces(device)
        qdef.save_connections(data)


if __name__ == "__main__":
    main()
