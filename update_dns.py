from __future__ import annotations

import http.client
import json
import logging
import sys
from os import getenv

import requests

logging.basicConfig(
    stream=sys.stdout,
    format='[CloudFlare DNS - %(asctime)s] %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S',
    level=logging.DEBUG,
)

# Web URL to get the public IP address
IP_API = 'https://api.ipify.org?format=json'

# Get CF API Key:
# https://support.cloudflare.com/hc/en-us/articles/200167836-Where-do-I-find-my-Cloudflare-API-key-
CF_API_TOKEN = getenv('CF_API_TOKEN')
# Your cloudflare email address
CF_EMAIL = getenv('CF_EMAIL')
# Your zone id is located on the main cloudflare domain dashboard
ZONE_ID = getenv('ZONE_ID')

# Domain you wish to import
DOMAIN = getenv('DOMAIN')

conn = http.client.HTTPSConnection('api.cloudflare.com')

resp = requests.get(IP_API)
ip = resp.json()['ip']

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {CF_API_TOKEN}',
}

# Get record ID
conn.request(
    'GET', f'/client/v4/zones/{ZONE_ID}/dns_records',
    body=None, headers=headers,
)

res = conn.getresponse()
data = json.loads(res.read())

proxied = False
type = 'A'
for items in data['result']:
    logging.info(
        f"Record ID for {items['name']} (type {items['type']}): \
            {items['id']} and proxied set to {items['proxied']}",
    )
    if items['name'] == DOMAIN:
        id = items['id']
        proxied = items['proxied']
        type = items['type']


payload = {
    'content': ip,
    'name': DOMAIN,
    'proxied': proxied,
    'type': type,
    'comment': f'Updating record for {DOMAIN} with IP {ip}',
    'tags': [],
    'ttl': 86400,
}

conn.request(
    'PUT', f'/client/v4/zones/{ZONE_ID}/dns_records/{id}',
    body=json.dumps(payload), headers=headers,
)

res = conn.getresponse()
if res.getcode() == 200:
    data = json.loads(res.read())
    logging.info(
        f"Record {data['result']['name']} has been updated to IP \
            {data['result']['content']}",
    )
else:
    logging.error('Error updating IP address, see more info below:')
    logging.error(res.read())
