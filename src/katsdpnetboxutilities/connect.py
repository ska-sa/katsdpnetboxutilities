import json
import logging
import time

from urllib.parse import urljoin
from pathlib import Path

import requests

from slugify import slugify

def _query_netbox(url, token, path, query=None):
    headers = {
        "Authorization": "Token {}".format(token),
        "Content-Type": "application/json",
        "Accept": "application/json; indent=4",
    }
    if query:
        query.setdefault('limit', 10000)
    req = requests.get(urljoin(url, path), headers=headers, params=query)
    return req.json()

def _query_netbox_url(url, path, query=None):
    if query:
        query.setdefault('limit', 1000)
    prepped = requests.Request('GET', urljoin(url, path), params=query).prepare()
    return prepped.url

def _load_cache(filename):
    if filename.is_file():
        age = time.time() - filename.stat().st_mtime
        if age < 36000:  # 10h # TODO: Make this a configuration value.
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
        data = _load_cache(cache_filename)

    if not data:
        data = _query_netbox(url, config["token"], path, query)

    if config["cache_path"]:
        _save_cache(data, cache_filename)

    return data
