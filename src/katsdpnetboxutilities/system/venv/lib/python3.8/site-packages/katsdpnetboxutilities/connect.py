import json
import logging
import requests
import time

from pathlib import Path
from slugify import slugify
from urllib.parse import urljoin

QUERY_LIMIT_DEFAULT = 10000


def _query_netbox(url, token, path, query=None):
    headers = {
        "Authorization": "Token {}".format(token),
        "Content-Type": "application/json",
        "Accept": "application/json; indent=4",
    }
    if query:
        query.setdefault("limit", QUERY_LIMIT_DEFAULT)
    req = requests.get(urljoin(url, path), headers=headers, params=query, verify=False)
    return req.json()


def _query_netbox_url(url, path, query=None):
    if query:
        query.setdefault("limit", QUERY_LIMIT_DEFAULT)
    prepped = requests.Request("GET", urljoin(url, path), params=query).prepare()
    return prepped.url


def _load_cache(filename, config={}, age=600):
    """
    config argument is depricated will be removed.
    """
    cache_age = config.get("cache_age", age)
    if filename.is_file():
        age = time.time() - filename.stat().st_mtime
        if age < (60 * cache_age):
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


def query_netbox(config, path, query=None, url=None, age=600, cache_path='/tmp'):
    data = None
    cache_path = config.get("cache_path", cache_path)
    cache_age = config.get("cache_age", age)
    url = config.get("url", url)

    if cache_path:
        filename = slugify(_query_netbox_url(url, path, query)) + ".json"
        cache_filename = Path(cache_path) / filename
        data = _load_cache(cache_filename, age=age)

    if not data:
        data = _query_netbox(url, config["token"], path, query)

    if config["cache_path"]:
        _save_cache(data, cache_filename)

    return data
