import requests
from bs4 import BeautifulSoup
import json

def get_bs_obj(url, headers=None, parser="html.parser"):
    if headers is None:
        result = requests.get(url)
    else:
        result = requests.get(url, headers=headers)

    print("Status Code: ", result.status_code)
    return BeautifulSoup(result.content, parser)

def get_json_object(url, headers=None):

    if headers is None:
        result = requests.get(url)
    else:
        result = requests.get(url, headers=headers)
    print("Status Code: ", result.status_code)
    return json.loads(result.content)