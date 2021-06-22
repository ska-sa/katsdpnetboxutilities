#!/usr/bin/env python3

import configargparse
import json
import logging
import requests

from boltons.strutils import bytes2human
from pathlib import Path
from pprint import pprint
from make_config import makeconfig

from katsdpnetboxutilities.connect import query_netbox


def format_bytes(size):
    # 2**10 = 1024
    size = int(size)
    power = 2 ** 10
    n = 0
    power_labels = {0: "", 1: "kilo", 2: "mega", 3: "giga", 4: "tera"}
    while size > power:
        size /= power
        n += 1
    if power_labels[n] == "kilo":
        suffix = "KB"
    elif power_labels[n] == "mega":
        suffix = "MB"
    elif power_labels[n] == "giga":
        suffix = "GB"
    elif power_labels[n] == "tera":
        suffix = "TB"
    else:
        suffix = ""
    return "{}{}".format(size, suffix)


class RemoteDeviceInfo:
    """Manage the fetching of data files from a remote source.

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
            data = {}
        return data

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
        self._lines.append("#" * level + " " + heading)
        self._lines.append(None)

    def text(self, text):
        self._lines.append(text)

    def ll_table(self, rows):
        """List-List no header table"""
        # Not a table just text now.
        self._lines.append(None)
        if "Site" in rows[0][0] or  "Status" in rows[0][0]:
            pass
        else:
            self._lines.append("**Specifications**\n")

        for row in rows:
            self._lines.append(f"\t - {row[0]} : **{row[1]}**\n".strip())
        self._lines.append(None)

    def write(self, filename):
        if filename:
            with open(filename, "w+") as fh:
                for line in self._lines:
                    if line:
                        fh.write(line)
                    fh.write("\n")
        else:
            output = ""
            for line in self._lines:
                if line:
                    output += line
                output += "\n"
            return output



class DeviceDocument:
    def __init__(self, netbox, device_info):
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
        self.page.heading("Netbox Information", 2)
        rows = []
        rows.append(self._get_value_for_table(self._netbox, "status"))
        rows.append(self._get_value_for_table(self._netbox, "id"))
        rows.append(
            (
                "Netbox URL",
                "[{}]({})".format(
                    self._get_value_for_table(self._netbox, "url")[1],
                    self._get_value_for_table(self._netbox, "url")[1],
                ),
            )
        )
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
        if cpu_info.get("disabled", False):
            self.page.text("CPU is disabled")
        else:
            rows.append(self._get_value_for_table(cpu_info, "vendor"))
            if self._get_value_for_table(cpu_info, "product") is not None:
                rows.append(self._get_value_for_table(cpu_info, "product"))
            elif self._get_value_for_table(cpu_info, "version") is not None:
                rows.append(self._get_value_for_table(cpu_info, "version"))
            if self._get_value_for_table(cpu_info, "clock") is not None:
                rows.append(
                    (
                        self._get_value_for_table(cpu_info, "clock")[0],
                        bytes2human(
                            int(self._get_value_for_table(cpu_info, "clock")[1]),
                            ndigits=2,
                        )
                        + "Hz",
                    )
                )
            elif self._get_value_for_table(cpu_info, "capacity") is not None:
                rows.append(
                    (
                        self._get_value_for_table(cpu_info, "capacity")[0],
                        bytes2human(
                            int(self._get_value_for_table(cpu_info, "capacity")[1]),
                            ndigits=2,
                        )
                        + "Hz",
                    )
                )
            cores_str = "enabled: {}/{}, threads {}".format(
                cpu_info["configuration"]["enabledcores"],
                cpu_info["configuration"]["cores"],
                cpu_info["configuration"]["threads"],
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
            if child.get("id") in [
                "memory",
                "memory:0",
                "memory:1",
                "memory:2",
                "memory:3",
                "memory:4",
                "memory:5",
                "memory:6",
            ]:
                # if "memory" in child.get("id"):
                memory = child
                break
        else:
            memory = {}

        memmap = {}
        for dimm in memory.get("children", []):
            if "vendor" in dimm and dimm["vendor"] != "NO DIMM":
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
            rows.append(
                (
                    self._get_value_for_table(memmap[slot], "size")[0],
                    format_bytes(self._get_value_for_table(memmap[slot], "size")[1]),
                )
            )
            rows.append(
                (
                    self._get_value_for_table(memmap[slot], "clock")[0],
                    str(
                        int(
                            self._get_value_for_table(memmap[slot], "clock")[1]
                            / 1000000
                        )
                    )
                    + "MHz",
                )
            )
            rows.append(self._get_value_for_table(memmap[slot], "serial"))
            self.page.ll_table(rows)

    def _add_disk(self):
        self.page.heading("Disks", 2)
        disks = self._device_info.lsblk_devices()
        for dev in sorted(disks.keys()):
            wwn = disks[dev].get("wwn")
            if wwn is not None:
                self.page.heading("WWN:" + disks[dev]["wwn"], 3)
                rows = []
                rows.append(self._get_value_for_table(disks[dev], "vendor"))
                rows.append(
                    self._get_value_for_table(disks[dev], "rota", "Spinning Disk")
                )
                rows.append(self._get_value_for_table(disks[dev], "model"))
                rows.append(
                    (
                        self._get_value_for_table(disks[dev], "size")[0],
                        format_bytes(self._get_value_for_table(disks[dev], "size")[1]),
                    )
                )
                rows.append(self._get_value_for_table(disks[dev], "serial"))
                self.page.ll_table(rows)
            else:
                logging.warning("Not adding device %s", disks[dev])

    def _add_fs(self):
        pass

    def write(self, filename: str = None):
        self.page.heading(self._netbox.get("name", "Server"), 1)
        self._add_general()
        self._add_location()
        self._add_disk()
        self._add_fs()
        self._add_cpu()
        self._add_memory()
        return self.page.write(filename)


def parse_args():
    """Parse command line, config file and environmental variables.

    See configargparse for more detail.
    """
    p = configargparse.ArgParser(default_config_files=["/.config/sarao/netbox"])
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


def host_report(hostname, settings):
    config = vars(settings)
    config["url"] = config["netbox_url"]
    config["token"] = config["netbox_token"]
    config["device_info"] = config["device_info_url"]
    config["device_name"] = hostname
    path = "/api/dcim/devices"
    query = {"name": config["device_name"]}
    netbox = query_netbox(config, path, query)
    if netbox and netbox.get("count") == 1:
        netbox = netbox["results"][0]
    else:
        logging.error("Could not get device")
    device_info = RemoteDeviceInfo(config["device_info"], config["device_name"])
    page = DeviceDocument(netbox, device_info)
    return page.write()


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
    filename = "{}/index.md".format(config["output_path"])
    device_info = RemoteDeviceInfo(config["device_info"], config["device_name"])
    page = DeviceDocument(netbox, device_info)
    makeconfig.make_header(config["device_name"])
    makeconfig.make_pandoc_yaml(config["device_name"])
    print(page)
    page.write(filename)


if __name__ == "__main__":
    main()
