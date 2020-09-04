from urllib.parse import urljoin

import requests


def query_netbox(url, token, path, query=None, cache_path=None):
    headers = {
        "Authorization": "Token {}".format(token),
        "Content-Type": "application/json",
        "Accept": "application/json; indent=4",
    }
    r = requests.get(urljoin(url, path), headers=headers, params=query)
    return r.json()
