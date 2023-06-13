import json
import requests


def api_call(link):
    response = requests.get(link, verify=False)
    if response.status_code == 200:
        data = response.text
        parse_json = json.loads(data)
    else:
        raise Exception(
            'There seems to be a issue getting your job recommendations back to you, please try again later')
    return parse_json


def key(e):
    return e['value']
