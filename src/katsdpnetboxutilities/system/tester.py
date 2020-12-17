import requests
import json

#token = "5c431a9daa31f13e31ac9deaaef65449a4059c72"

#headers = {
#    "Authorization": "Token 5c431a9daa31f13e31ac9deaaef65449a4059c72",
#    "Content-Type": "application/json",
#    "Accept": "application/json; indent=4",
#}

url = "https://netboxtest.sdp.kat.ac.za"
#tail = "/api/dcim/interfaces/?device_id=123"
#response = requests.get(url, headers=headers, verify=False)
#print(response.text)
#all_results = json.loads(response.text)['results']

#print(all_results)

import pynetbox

session = requests.Session()
session.verify = False
nb = pynetbox.api(url,
                  token='5c431a9daa31f13e31ac9deaaef65449a4059c72'
                  )
nb.http_session = session
print(nb.dcim.devices.all())