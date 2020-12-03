import json
import logging
import time

from urllib.parse import urljoin
from pathlib import Path

import requests

from slugify import slugify

QUERY_LIMIT_DEFAULT = 10000

# OLD style
def _query_netbox(url, token, path=None, query=None):
    headers = {
        "Authorization": "Token {}".format(token),
        "Content-Type": "application/json",
        "Accept": "application/json; indent=4",
    }
    if query:
        query.setdefault("limit", QUERY_LIMIT_DEFAULT)
    req = requests.get(urljoin(url, path), headers=headers, params=query)
    return req.json()


def _query_netbox_url(url, path=None, query=None):
    if query:
        query.setdefault("limit", QUERY_LIMIT_DEFAULT)
    prepped = requests.Request("GET", urljoin(url, path), params=query).prepare()
    return prepped.url


def _load_cache(filename, config):
    if filename.is_file():
        age = time.time() - filename.stat().st_mtime
        if age < (60 * config["cache_age"]):
            with open(filename) as fh:
                logging.info("Reading results from %s", filename)
                return json.load(fh)


def _save_cache(data, filename):
    if data:
        with open(filename, "w+") as fh:
            logging.info("Saving results to %s", filename)
            json.dump(data, fh)
    else:
        logging.debug("SaveCache: Missing data, nothing cached.")


def query_netbox(config, path, query=None):
    data = None
    url = config["url"]

    if config["cache_path"]:
        filename = slugify(_query_netbox_url(url, path, query)) + ".json"
        cache_filename = Path(config["cache_path"]) / filename
        data = _load_cache(cache_filename, config)

    if not data:
        data = _query_netbox(url, config["token"], path, query)

    if config["cache_path"]:
        _save_cache(data, cache_filename)

    return data

# New style


class NetboxConnection:

    def __init__(self, config):
        self.config = config

    def _cache_load(self, filename):
        if filename.is_file():
            age = time.time() - filename.stat().st_mtime
            if age < (60 * float(self.config["cache_age"])):
                with open(filename) as fh:
                    logging.debug("_cache_load from %s", filename)
                    return json.load(fh)

    def _cache_save(self, filename, data):
        if data:
            with open(filename, "w+") as fh:
                logging.debug("_cache_save to %s", filename)
                json.dump(data, fh)
        else:
            logging.debug("_cache_save: Missing data, nothing cached.")

    def query_path(self, path, query=None, url=None):
        data = None
        if url is None:
           url = self.config["url"]

        if self.config["cache_path"]:
            filename = slugify(_query_netbox_url(url, path, query)) + ".json"
            cache_filename = Path(self.config["cache_path"]) / filename
            data = self._cache_load(cache_filename)

        if not data:
            data = _query_netbox(url, self.config["token"], path, query)

        if self.config["cache_path"]:
            self._cache_save(cache_filename, data)

        return data

    def ipaddresses(self, selection: dict=None, key:str=None, value:str=None):
        # TODO: this method and devices are the same. Merge the code.
        path = "/api/ipam/ip-addresses"
        if selection is None:
            selection = {}

        if key and value:
            if value.startswith('id:'):
                selection[key + '_id'] = int(value.split(':')[1])
            elif type(value) == int:
                selection[key + '_id'] = value
            else:
                selection[key] = value

        data = self.query_path(path, query=selection)
        for result in data.get('results', []):
            yield result
        # Check data['next'] if it exists Query that url.
        while data.get('next'):
            data = self.query_path(path=None, url=data['next'], query=selection)
            for result in data.get('results', []):
                yield result

    def devices(self, selection: dict=None, key:str=None, value:str=None):
        path = "/api/dcim/devices"
        if selection is None:
            selection = {}

        if key and value:
            if value.startswith('id:'):
                selection[key + '_id'] = int(value.split(':')[1])
            elif type(value) == int:
                selection[key + '_id'] = value
            else:
                selection[key] = value

        data = self.query_path(path, query=selection)
        for result in data.get('results', []):
            yield result
        # Check data['next'] if it exists Query that url.
        while data.get('next'):
            data = self.query_path(path=None, url=data['next'], query=selection)
            for result in data.get('results', []):
                yield result

    def device_interfaces(self, device):
        query =  {"device": device}
        if type(device) == int:
            query =  {"device_id": device}
        elif device.startswith('id:'):
            device_id = int(device.split(':')[1])
            query =  {"device_id": device_id}
        path = "/api/dcim/interface-connections"
        data = self.query_path(path, query)
        return data

    def lookup_device_ids(self, device_name):
        query = {'name': device_name}
        path = "/api/dcim/devices"
        data = self.query_path(path, query)
        if data['count'] > 1:
            logging.warning("While looking for device %s we found %s devices.", device_name, data['count'])
        for device in data.get('results', []):
            yield device['id']
