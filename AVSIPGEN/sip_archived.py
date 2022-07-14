# This script searches across a defined range of SIP IDs and reports any that are
# Archived i.e. SIPs that have been deleted by a user in the SIP Tool using the
# Remove button
# Script requires config.py to run

from requests.packages import urllib3
import requests
import json
import config

# Mutes SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# API reference: GET api/SIP/{id}
# https://avsip.ad.bl.uk/Help/Api/GET-api-SIP-id

url = config.url

archived_id = 'archived_SIPs.txt'

# Set the range of SIP IDs to search
sip = 120000
while sip <= 120874:
    scrape = '{}/SIP/{}'.format(url, str(sip))
    r = requests.get(scrape, verify=False)

    if r:
        data = json.loads(r.text)
        arch = data['Archived']
        cn = data['SamiCallNumber']

        if arch == True:
            with open(archived_id, 'a') as removed_sips:
                removed_sips.write('{}'.format(sip) + '\n')
                print('Archived: {} - {}'.format(sip, cn))

    sip += 1
