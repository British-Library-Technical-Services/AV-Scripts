# This script searches across a defined range of SIP IDs and reports the step they
# have been completed upto.  The search excludes those submitted for ingest and Archvied SIPs
# Script requires config.py to run

from requests.packages import urllib3
import requests
import json
import config

# Mutes SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SIPStatus = 'sip_status.txt'
url = config.url

# Set the range of SIP IDs to search
sip = 1
while sip <= 25:
    scrape = '{}/SIP/{}'.format(url, str(sip))
    r = requests.get(scrape, verify=False)
    if r:
        data = json.loads(r.text)
        cn = data['SamiCallNumber']
        ss = data['StepStates']

        for stat in ss:
            sipid = stat['SIPId']
            step = stat['StepId']
            com = stat['Complete']

# SIP steps are numbered 1,2,3,20,4,15,5,6 in the json output
# the numbering is adjusted to the correct sequencial order for clarity
            if com == False:
                if step == 20:
                    step = 4
                elif step == 4:
                    step = 5
                elif step == 15:
                    step = 6
                elif step == 5:
                    step = 7
                elif step == 6:
                    step = 8

                step = step -1

# writes the unfinished SIPs to a sip_status text file
                with open(SIPStatus, 'a') as step_no:
                    step_no.write('{};{};{}'.format(step, sipid, cn) + '\n')
                    print('ID: {}; Shelfmark: {}; Steps complete: {}'.format(sipid, cn, step))
                    break
            else:
                continue
    sip += 1

print('Complete')
input()
