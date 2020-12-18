#!/usr/bin/env python3

import configargparse
import json
import logging
import pynetbox
import requests

from pathlib import Path
from pprint import pprint

from katsdpnetboxutilities.connect import query_netbox


class Page:

    def __init__(self):
        self._lines = []

    def heading(self, heading, level):
        c = {1: "#",
             2: "*",
             3: "="}.get(level, '=')
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
            self._lines.append(f"   * - {row[0]}")
            self._lines.append(f"     - {row[1] if row[1] else ''}")
        self._lines.append(None)

    def write(self, filename):
        with open(filename, 'w+') as fh:
            for line in self._lines:
                if line:
                    fh.write(line)
                fh.write('\n')


class DeviceDocument:

    def __init__(self, filename, netbox, lshw, lsblk):
        self.filename = filename
        self._netbox = netbox
        self._lshw = lshw
        self._lsblk = lsblk  # lsblk must be called with -fs flag.
        self.page = Page()

    def _get_value_for_table(self, src, key, label=None):
        if label is None:
            label = key.title().replace("_", " ")
        value = None
        _val = src.get(key)
        if type(_val) is dict:
            if 'display_name' in _val:
                value = _val['display_name']
            elif 'name' in _val:
                value = _val['name']
            else:
                value = _val.get('label')
        else:
            value = _val
        return label, value

    def _add_general(self):
        rows = []
        rows.append(self._get_value_for_table(self._netbox, 'status'))
        rows.append(self._get_value_for_table(self._netbox, 'serial'))
        rows.append(self._get_value_for_table(self._netbox, 'device_role'))
        rows.append(self._get_value_for_table(self._netbox, 'device_type'))
        self.page.ll_table(rows)

    def _add_location(self):
        self.page.heading('Location', 2)

        rows = []
        rows.append(self._get_value_for_table(self._netbox, 'site'))
        rows.append(self._get_value_for_table(self._netbox, 'rack'))
        rows.append(self._get_value_for_table(self._netbox, 'position', 'U'))
        rows.append(self._get_value_for_table(self._netbox, 'face'))
        self.page.ll_table(rows)

    # {'id': 'cpu:0', 'class': 'processor', 'claimed': True, 'handle': 'DMI:001F', 'description': 'CPU', 'product': 'AMD EPYC 7371 16-Core Processor', 'vendor': 'Advanced Micro Devices [AMD]', 'physid': '1f', 
    #'businfo': 'cpu@0', 'version': 'AMD EPYC 7371 16-Core Processor', 'serial': 'Unknown', 'slot': 'CPU1', 'units': 'Hz', 'size': 3780275000, 'capacity': 3800000000, 'width': 64, 'clock': 100000000, 
    #'configuration': {'cores': '16', 'enabledcores': '16', 'threads': '32'}, 
    #'capabilities': {'x86-64': '64bits extensions (x86-64)', 'fpu': 'mathematical co-processor', 'fpu_exception': 'FPU exceptions reporting', 'wp': True, 'vme': 'virtual mode extensions', 'de': 'debugging extensions', 'pse': 'page size extensions', 'tsc': 'time stamp counter', 'msr': 'model-specific registers', 'pae': '4GB+ memory addressing (Physical Address Extension)', 'mce': 'machine check exceptions', 'cx8': 'compare and exchange 8-byte', 'apic': 'on-chip advanced programmable interrupt controller (APIC)', 'sep': 'fast system calls', 'mtrr': 'memory type range registers', 'pge': 'page global enable', 'mca': 'machine check architecture', 'cmov': 'conditional move instruction', 'pat': 'page attribute table', 'pse36': '36-bit page size extensions', 'clflush': True, 'mmx': 'multimedia extensions (MMX)', 'fxsr': 'fast floating point save/restore', 'sse': 'streaming SIMD extensions (SSE)', 'sse2': 'streaming SIMD extensions (SSE2)', 'ht': 'HyperThreading', 'syscall': 'fast system calls', 'nx': 'no-execute bit (NX)', 'mmxext': 'multimedia extensions (MMXExt)', 'fxsr_opt': True, 'pdpe1gb': True, 'rdtscp': True, 'constant_tsc': True, 'rep_good': True, 'nopl': True, 'nonstop_tsc': True, 'cpuid': True, 'extd_apicid': True, 'amd_dcm': True, 'aperfmperf': True, 'pni': True, 'pclmulqdq': True, 'monitor': True, 'ssse3': True, 'fma': True, 'cx16': True, 'sse4_1': True, 'sse4_2': True, 'movbe': True, 'popcnt': True, 'aes': True, 'xsave': True, 'avx': True, 'f16c': True, 'rdrand': True, 'lahf_lm': True, 'cmp_legacy': True, 'svm': True, 'extapic': True, 'cr8_legacy': True, 'abm': True, 'sse4a': True, 'misalignsse': True, '3dnowprefetch': True, 'osvw': True, 'skinit': True, 'wdt': True, 'tce': True, 'topoext': True, 'perfctr_core': True, 'perfctr_nb': True, 'bpext': True, 'perfctr_llc': True, 'mwaitx': True, 'cpb': True, 'hw_pstate': True, 'ssbd': True, 'ibpb': True, 'vmmcall': True, 'fsgsbase': True, 'bmi1': True, 'avx2': True, 'smep': True, 'bmi2': True, 'rdseed': True, 'adx': True, 'smap': True, 'clflushopt': True, 'sha_ni': True, 'xsaveopt': True, 'xsavec': True, 'xgetbv1': True, 'xsaves': True, 'clzero': True, 'irperf': True, 'xsaveerptr': True, 'arat': True, 'npt': True, 'lbrv': True, 'svm_lock': True, 'nrip_save': True, 'tsc_scale': True, 'vmcb_clean': True, 'flushbyasid': True, 'decodeassists': True, 'pausefilter': True, 'pfthreshold': True, 'avic': True, 'v_vmsave_vmload': True, 'vgif': True, 'overflow_recov': True, 'succor': True, 'smca': True, 'cpufreq': 'CPU Frequency scaling'}}, 
    def _add_cpu_table(self, cpu_info):
        rows = []
        rows.append(self._get_value_for_table(cpu_info, 'vendor'))
        rows.append(self._get_value_for_table(cpu_info, 'product'))  # or version
        rows.append(self._get_value_for_table(cpu_info, 'capacity', 'Clock'))  # The Max clock
        cores_str = f"enabled: {cpu_info['configuration']['enabledcores']}/{cpu_info['configuration']['cores']}, " \
                    f"threads {cpu_info['configuration']['threads']}"
        rows.append(('Cores', cores_str))
        capabilities = []
        for cap, val in cpu_info['capabilities'].items():
            if val is True:
                capabilities.append(cap)
            else:
                capabilities.append(val)
        rows.append(('Capabilities', ", ".join(sorted(capabilities))))
        self.page.ll_table(rows)

    def _add_cpu(self):
        # .[0].children[0].children[1]
        self.page.heading("CPU", 2)
        cpus = {}
        core = self._lshw_core()
        for child in core.get('children', []):
            if child.get('id') in ['cpu', 'cpu:0', 'cpu:1']:
                cpus[child['slot']] = child
        print(cpus)
        if 'cpu' in cpus:
            # Single CPU system
            self._add_cpu_table(cpus['cpu'])
        else:
            for cpu in sorted(cpus.keys()):
                self.page.heading(cpu, 3)
                self._add_cpu_table(cpus[cpu])

    def _lshw_core(self):
        for child in self._lshw.get('children', []):
            if child.get('id') == 'core':
                return child
        return {}

    def _add_memory(self):
        # .[0].children[0].children[1]
        self.page.heading("Memory", 2)
        core = self._lshw_core()
        for child in core.get('children', []):
            if child.get('id') == 'memory':
                memory = child
                break
        else:
            memory = None

        memmap = {}
        for dimm in memory.get('children', []):
            if dimm['vendor'] != 'NO DIMM':
                memmap[dimm['slot']] = dimm

        # TODO: Total Memory
        # {'id': 'bank:0', 'class': 'memory', 'claimed': True, 'handle': 'DMI:003F', 'description': 'SODIMM DDR4 Synchronous 2667 MHz (0.4 ns)', 
        # 'product': '8ATF1G64HZ-2G6E1', 'vendor': 'Micron Technology', 'physid': '0', 'serial': '1C4A8B4C', 'slot': 'DIMM A', 
        # 'units': 'bytes', 'size': 8589934592, 'width': 64, 'clock': 2667000000},)'
        for slot in sorted(memmap.keys()):
            self.page.heading(slot, 3)
            rows = []
            rows.append(self._get_value_for_table(memmap[slot], 'description'))
            rows.append(self._get_value_for_table(memmap[slot], 'vendor'))
            rows.append(self._get_value_for_table(memmap[slot], 'product'))
            rows.append(self._get_value_for_table(memmap[slot], 'size'))
            rows.append(self._get_value_for_table(memmap[slot], 'clock'))
            rows.append(self._get_value_for_table(memmap[slot], 'serial'))
            self.page.ll_table(rows)

    def _add_disk(self):
        self.page.heading("Disks", 2)
        disks = self._lsblk['devices']
        for dev in sorted(disks.keys()):
            self.page.heading("WWN:" + disks[dev]['wwn'], 3)
            rows = []
            #rows.append(self._get_value_for_table(disks[dev], 'wwn'))
            rows.append(self._get_value_for_table(disks[dev], 'rota', 'Spinning Disk'))
            rows.append(self._get_value_for_table(disks[dev], 'model'))
            rows.append(self._get_value_for_table(disks[dev], 'size'))
            rows.append(self._get_value_for_table(disks[dev], 'serial'))
            self.page.ll_table(rows)

    def _add_fs(self):
        pass

    def write(self):
        self.page.heading(self._netbox['name'], 1)  
        self._add_general()
        self._add_location()
        self._add_disk()
        self._add_fs()
        #self._add_cpu()
        #self._add_memory()
        self.page.write(self.filename)


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
    #p.add("-n", "--name", required=True, help="Graph name")  # TODO: Not required anymore
    p.add("-v", "--verbose", help="Verbose", action="store_true")
    p.add("-d", "--debug", help="Debug", action="store_true")
    p.add("--device", help="Netbox device name from Ansible {{ inventroy_hostname }}")
    p.add("--lsblk", help="lsblk location")
    p.add("--lshw", help="lshw location")

    # URL should contain a directory of system names
    # If no documents found just give warning and continue
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


def get_lshw():
    pfile = Path('lshw.json')
    data = {}
    if pfile.exists():
        with pfile.open() as pfh:
            data = json.load(pfh)
    if type(data) == list:
        data = data[0]
    return data


def get_lsblk ():
    pfile = Path('lsblk.json')
    data = {}
    if pfile.exists():
        with pfile.open() as pfh:
            data = json.load(pfh)
    if type(data) == list:
        data = data[0]

    data['partitions'] = {}
    data['devices'] = {}
    for blkdev in data.get('blockdevices', []):
        pprint(blkdev)
        if blkdev.get('type') not in ['loop']:
            data['devices'][blkdev['name']] = blkdev
            for dev in blkdev.get('children', []):
                data['partitions'][dev['name']] = dev

    return data


def get_netbox_device_id(url, token, hostname):
    session = requests.Session()
    session.verify = False
    nb = pynetbox.api(url,
                      token=token
                      )
    nb.http_session = session
    response = nb.dcim.devices.get(name=hostname)
    device_dict = dict(response)
    device_id = device_dict.get('id')
    return device_id


def main():
    config = parse_args()
    pprint(config)
    id = get_netbox_device_id(config["url"], config["token"], config["device"])
    path = f"/api/dcim/devices/{id}/"
    print(f"path = {path}")
    query = {}
    netbox = query_netbox(config, path, query)
    filename = f"{config['output_path']}/index.rst"
    page = DeviceDocument(filename, netbox, get_lshw(), get_lsblk())
    print(page)
    page.write()


if __name__ == "__main__":
    main()
