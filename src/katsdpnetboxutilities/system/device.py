#!/usr/bin/env python3

import configargparse
import json
import logging
import requests

from pathlib import Path
from pprint import pprint

from katsdpnetboxutilities.connect import query_netbox


class RemoteDeviceInfo:
    """Manage the fetching of data files from a remote sorce.

    This class holds the normalisation code for the different datatypes.
    e.g., manages the small differences in format caused by the different version of the collection tools.

    """

    def __init__(self, url, device_name):
        self.url = url or None
        self.device_name = device_name
        self._cache = {}

    def a_get_lshw(self):
        pfile = Path("lshw.json")
        data = {}
        if pfile.exists():
            with pfile.open() as pfh:
                data = json.load(pfh)
        if type(data) == list:
            data = data[0]
        return data

    def a_get_lsblk(self):
        pfile = Path("lsblk.json")
        data = {}
        if pfile.exists():
            with pfile.open() as pfh:
                data = json.load(pfh)
        if type(data) == list:
            data = data[0]
        data["partitions"] = {}
        data["devices"] = {}
        for blkdev in data.get("blockdevices", []):
            pprint(blkdev)
            if blkdev.get("type") not in ["loop"]:
                data["devices"][blkdev["name"]] = blkdev
                for dev in blkdev.get("children", []):
                    data["partitions"][dev["name"]] = dev

        return data

    def _remote_get(self, path, filename, is_json=True):
        if path:
            _url = "{}/{}/{}".format(
                self.url.strip("/"), path.strip("/"), filename.strip("/")
            )
        else:
            _url = "{}/{}".format(self.url.strip("/"), filename.strip("/"))
        req = requests.get(_url)
        if req.status_code == requests.codes.ok:
            if is_json:
                return req.json()
            else:
                return req.body
        else:
            logging.warning("Could not load - %s", _url)

    def get_file_from_remote(self, filename, is_json=True):
        # TODO: fix the retry
        if self.url is None:
            logging.warning("No remote server defined, not fetching from remote.")
            return {}
        data = self._remote_get(self.device_name, filename, is_json)
        if data is None:
            data = self._remote_get(
                "servers/{}".format(self.device_name), filename, is_json
            )
        if data is None:
            data = self._remote_get(None, filename, is_json)
        if not data:
            logging.warning("No %s found on %s", filename, self.url)
        return data or {}

    def get_lshw(self) -> dict:
        lshw = self._cache.get("lshw")
        if lshw is None:
            lshw = self.get_file_from_remote("lshw.json")
            self._cache["lshw"] = lshw
        return lshw or {}

    def get_lsblk(self) -> dict:
        lsblk = self._cache.get("lsblk")
        if lsblk is None:
            lsblk = self.get_file_from_remote("lsblk.json")
            self._cache["lsblk"] = lsblk
        return lsblk or {}

    def lshw_core(self):
        """Helper method to return only the lshw core"""
        lshw = self.get_lshw()
        for child in lshw.get("children", []):
            if child.get("id") == "core":
                return child
        return {}

    def lsblk_devices(self):
        lsblk = self.get_lsblk()
        data = {}
        for blkdev in lsblk.get("blockdevices", []):
            pprint(blkdev)
            if blkdev.get("type") not in ["loop"]:
                data[blkdev["name"]] = blkdev
        return data

class Page:
    def __init__(self):
        self._lines = []

    def heading(self, heading, level):
        c = {1: "#", 2: "*", 3: "="}.get(level, "=")
        self._lines.append(heading)
        self._lines.append(c * len(heading))
        self._lines.append(None)

    def text(self, text):
        self._lines.append(text)

    def ll_table(self, rows):
        """List-List no header table"""
        # Not a table just text now.
        self._lines.append(None)
        self._lines.append(".. list-table::")
        self._lines.append("   :widths: 10 25")
        self._lines.append("   :header-rows: 0")
        self._lines.append(None)
        for row in rows:
            self._lines.append("   * - {}".format(row[0]))
            self._lines.append("     - {}".format(row[1] if row[1] else ''))
        self._lines.append(None)

    def write(self, filename):
        with open(filename, "w+") as fh:
            for line in self._lines:
                if line:
                    fh.write(line)
                fh.write("\n")


class DeviceDocument:
    def __init__(self, filename, netbox, device_info):
        self.filename = filename
        self._netbox = netbox
        self._device_info = device_info
        self.page = Page()

    def _get_value_for_table(self, src, key, label=None):
        if label is None:
            label = key.title().replace("_", " ")
        value = None
        _val = src.get(key)
        if type(_val) is dict:
            if "display_name" in _val:
                value = _val["display_name"]
            elif "name" in _val:
                value = _val["name"]
            else:
                value = _val.get("label")
        else:
            value = _val
        return label, value

    def _add_general(self):
        rows = []
        rows.append(self._get_value_for_table(self._netbox, "status"))
        rows.append(self._get_value_for_table(self._netbox, "serial"))
        rows.append(self._get_value_for_table(self._netbox, "device_role"))
        rows.append(self._get_value_for_table(self._netbox, "device_type"))
        self.page.ll_table(rows)

    def _add_location(self):
        self.page.heading("Location", 2)

        rows = []
        rows.append(self._get_value_for_table(self._netbox, "site"))
        rows.append(self._get_value_for_table(self._netbox, "rack"))
        rows.append(self._get_value_for_table(self._netbox, "position", "U"))
        rows.append(self._get_value_for_table(self._netbox, "face"))
        self.page.ll_table(rows)

    def _add_cpu_table(self, cpu_info):
        rows = []
        rows.append(self._get_value_for_table(cpu_info, "vendor"))
        rows.append(self._get_value_for_table(cpu_info, "product"))  # or version
        rows.append(
            self._get_value_for_table(cpu_info, "capacity", "Clock")
        )  # The Max clock
        cores_str = (
            "enabled: {}/{}, threads {}".format(
                cpu_info['configuration']['enabledcores'],
                cpu_info['configuration']['cores'],
                cpu_info['configuration']['threads']
            )
        )
        rows.append(("Cores", cores_str))
        capabilities = []
        for cap, val in cpu_info["capabilities"].items():
            if val is True:
                capabilities.append(cap)
            else:
                capabilities.append(val)
        rows.append(("Capabilities", ", ".join(sorted(capabilities))))
        self.page.ll_table(rows)

    def _add_cpu(self):
        # .[0].children[0].children[1]
        self.page.heading("CPU", 2)
        cpus = {}
        core = self._device_info.lshw_core()
        for child in core.get("children", []):
            if child.get("id") in ["cpu", "cpu:0", "cpu:1"]:
                cpus[child["slot"]] = child
        print(cpus)
        if "cpu" in cpus:
            # Single CPU system
            self._add_cpu_table(cpus["cpu"])
        else:
            for cpu in sorted(cpus.keys()):
                self.page.heading(cpu, 3)
                self._add_cpu_table(cpus[cpu])

    def _add_memory(self):
        # .[0].children[0].children[1]
        self.page.heading("Memory", 2)
        core = self._device_info.lshw_core()
        for child in core.get("children", []):
            if child.get("id") == "memory":
                memory = child
                break
        else:
            memory = None

        memmap = {}
        for dimm in memory.get("children", []):
            if 'vendor' in dimm and dimm["vendor"] != "NO DIMM":
                memmap[dimm["slot"]] = dimm

        # TODO: Total Memory
        # {'id': 'bank:0', 'class': 'memory', 'claimed': True, 'handle': 'DMI:003F', 'description': 'SODIMM DDR4 Synchronous 2667 MHz (0.4 ns)',
        # 'product': '8ATF1G64HZ-2G6E1', 'vendor': 'Micron Technology', 'physid': '0', 'serial': '1C4A8B4C', 'slot': 'DIMM A',
        # 'units': 'bytes', 'size': 8589934592, 'width': 64, 'clock': 2667000000},)'
        for slot in sorted(memmap.keys()):
            self.page.heading(slot, 3)
            rows = []
            rows.append(self._get_value_for_table(memmap[slot], "description"))
            rows.append(self._get_value_for_table(memmap[slot], "vendor"))
            rows.append(self._get_value_for_table(memmap[slot], "product"))
            rows.append(self._get_value_for_table(memmap[slot], "size"))
            rows.append(self._get_value_for_table(memmap[slot], "clock"))
            rows.append(self._get_value_for_table(memmap[slot], "serial"))
            self.page.ll_table(rows)

    def _add_disk(self):
        self.page.heading("Disks", 2)
        disks = self._device_info.lsblk_devices()
        for dev in sorted(disks.keys()):
            wwn = disks[dev].get('wwn')
            if wwn is not None:
                self.page.heading("WWN:" + disks[dev]["wwn"], 3)
                rows = []
                rows.append(self._get_value_for_table(disks[dev], "rota", "Spinning Disk"))
                rows.append(self._get_value_for_table(disks[dev], "model"))
                rows.append(self._get_value_for_table(disks[dev], "size"))
                rows.append(self._get_value_for_table(disks[dev], "serial"))
                self.page.ll_table(rows)
            else:
                logging.warning("Not adding device %s", disks[dev])

    def _add_fs(self):
        pass

    def write(self):
        self.page.heading(self._netbox["name"], 1)
        self._add_general()
        self._add_location()
        self._add_disk()
        self._add_fs()
        self._add_cpu()
        self._add_memory()
        self.page.write(self.filename)


def parse_args():
    """Parse command line, config file and environmental variables.

    See configargparse for more detail.
    """
    p = configargparse.ArgParser(default_config_files=["~/.config/sarao/netbox"])
    p.add("-c", "--config", is_config_file=True, help="config file")
    p.add("--token", help="Netbox connection token")
    p.add("--url", help="Netbox server URL")
    p.add("--cache-path", help="Directory to store temporary (cached) results")
    p.add("--cache-age", help="How old cached objects can get, in minutes", default=600)
    p.add(
        "-o",
        "--output-path",
        required=True,
        help="Path where the output files will be stored",
    )
    p.add("-v", "--verbose", help="Verbose", action="store_true")
    p.add("-d", "--debug", help="Debug", action="store_true")
    p.add("--device-info", help="URL where device info files can be found")
    p.add("device_name", nargs=1, type=str, help="Device name")
    # URL should contain a directory of system names
    # If no documents found just give warning and continue

    config = vars(p.parse_args())
    config["device_name"] = config["device_name"][0]  # Unwind the list

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
    pprint(config)
    path = "/api/dcim/devices"
    query = {"name": config["device_name"]}
    netbox = query_netbox(config, path, query)
    if netbox and netbox.get("count") == 1:
        netbox = netbox["results"][0]
    else:
        logging.error("Could not get device")
    filename = "{}/source/{}/index.rst".format(
        config['output_path'],
        config['device_name']
    )
    device_info = RemoteDeviceInfo(config["device_info"], config['device_name'])
    page = DeviceDocument(filename, netbox, device_info)
    print(page)
    page.write()


if __name__ == "__main__":
    main()
