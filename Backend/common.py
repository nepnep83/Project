import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def api_call(link):
    response = requests.get(link, verify=False)
    if response.status_code == 200:
        return json.loads(response.text)
    elif response.status_code == 503:
        return "too many calls"
    elif response.status_code == 400:
        return "not found"
    else:
        raise Exception(
            'There seems to be a issue getting your job recommendations back to you, please try again later')


def key(e):
    return e['value']
