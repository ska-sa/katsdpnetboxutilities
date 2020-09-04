import re
import os
import json
import logging

from urllib.parse import urljoin

import requests


def _query_netbox(url, token, path, query=None):
    headers = {
        "Authorization": "Token {}".format(token),
        "Content-Type": "application/json",
        "Accept": "application/json; indent=4",
    }
    r = requests.get(urljoin(url, path), headers=headers, params=query)
    return r.json()


def query_netbox(config, path, query=None):
    # TODO: add cache expire after 1Day.
    if config["cache_path"]:
        filename = path + "_"
        if query:
            filename += "_".join(["{}={}".format(k, v) for k, v in query.items()])
        filename = re.sub(r"[\W_]+", "_", filename)
        cache_filename = os.path.join(
            config["cache_path"], filename.strip("_") + ".json"
        )
        if os.path.isfile(cache_filename):
            with open(cache_filename) as fh:
                logging.info("Reading results from %s", cache_filename)
                return json.load(fh)
        else:
            data = _query_netbox(config["url"], config["token"], path, query)
            with open(cache_filename, "w+") as fh:
                logging.info("Saving results to %s", cache_filename)
                json.dump(data, fh)
            return data

    else:
        data = _query_netbox(config["url"], config["token"], path, query)
    return data
