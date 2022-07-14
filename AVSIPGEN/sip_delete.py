# This script will delete SIPs from a list of IDs in the SIPstoDelete.txt file
# WARNING: this will erase all reference to the SIP in the tool and database
# and it will delete any files associated with the SIP.  Use with care - the
# process is not reversable
# Script requires config.py to run

from requests.packages import urllib3
import requests
import json
import os
import config

# Mutes SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

list = 'SIPstoDelete.txt'
url = config.url
user = config.user
hold = config.hold

with open(list, 'r') as del_list:
    for sip in del_list:
        sip = sip.rstrip()

        check_url = '{}/SIP/{}/'.format(url, sip)
        c = requests.get(check_url, verify=False)
        status = c.status_code
        if status == 200:

            del_url = '{}/SIPs/SIP/{}/{}'.format(url, user, sip)
            d = requests.delete(del_url, verify=False)

            sip_folder = '\\{}\{}'.format(hold, sip)

# Checks the SIP has been deleted (page returns a 404 error) and removes
# the SIP directory on SOS_HLF\_hold if stll present

            check = requests.get(check_url, verify=False)
            if check.status_code == 404:
                if os.path.exists(sip_folder):
                    try:
                        os.rmdir(sip_folder)
                        print('{} DELETED'.format(sip))
                    except Exception as e:
                        print('{}: exception raised {}'.format(sip, e))
                else:
                    print('{} DELETED'.format(sip))

            else:
                get_error = json.loads(d.text)
                error = get_error['Errors']
                print('{} unable to delete {}'.format(sip, error))

        elif status == 404:
            print('{} does not exist'.format(sip))
        else:
            print('{} unable to to delete, returning status code: {}'.format(status))
