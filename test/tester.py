#!/usr/bin/env python3

from pprint import pprint
import json

with open("../test/files/lshw.json", 'r') as handle:
    parsed = json.load(handle)

print(json.dumps(parsed, indent=4, sort_keys=True))

