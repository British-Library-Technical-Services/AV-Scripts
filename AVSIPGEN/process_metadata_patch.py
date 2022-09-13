# This script will copy the process metadata from one SIP (src_sip_id) to another (dest_sip_id)
# A gui version is available to download from [url]
# The script requires config.py to run

# API reference: GET api/SIP/processmetadata/{id}
# API reference: PATCH api/SIP/processmetadata/{sip_id}/{stepstate_id}/{user_id}/{mark_step_complete}

from requests.packages import urllib3
import requests
import json
import config

# Mutes SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = config.url

# Set source SIP the process metadata will be copied from
src_sip_id = '125926'

# Set destination SIP the process metadata will be copied to
dest_sip_id = '126332'

# Function to capture process metadata from source SIP
def statusCheck(src_sip_id):
    src_url = "{}/SIP/{}".format(url, src_sip_id)
    src_get = requests.get(src_url, verify=False)
    status = src_get.status_code
    
    if status == 200:
        print('{}: SIP ID OKAY'.format(status))
        patchPM(src_get, dest_sip_id)
    else:
        print('{}: ERROR'.format(status))

# Function to Patch (copy) the process metadata to the destination SIP
def patchPM(src_get, dest_sip_id):
    src_get.encoding = src_get.apparent_encoding
    src_json = src_get.json()

    d = json.loads(src_json['ProcessMetadata'])

    dest_url = '{}/SIP/{}'.format(url, dest_sip_id)
    dest_req = requests.get(dest_url, verify=False)
    dest_json = dest_req.json()

    dest_process_metadata = json.dumps(d)
    dest_user_id = dest_json['UserId']

    for x in dest_json['StepStates']:
        if x['StepTitle'] == 'Process Metadata':
            dest_step_id = x['StepStateId']

    patch_url = '{}/SIP/processmetadata/{}/{}/{}/true'.format(
        url,
        dest_sip_id,
        dest_step_id,
        dest_user_id
        )

    r = requests.patch(
        patch_url,
        json=dest_process_metadata,
        verify=False
        )
    print('{} >>> {} Complete'.format(src_sip_id, dest_sip_id))

statusCheck(src_sip_id)
