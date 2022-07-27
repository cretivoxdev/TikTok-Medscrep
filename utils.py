import random
import string
import requests
import json


def random_key(length):
    key = ''
    for i in range(length):
        key += random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
    return key


def build_get_url(base_url, params, append=False):
    final_url = base_url
    if append:
        final_url += "&"
    else:
        final_url += "?"
    for key, val in params.items():
        final_url += key + "=" + val + "&"
    final_url = final_url[:-1]
    return final_url


def get_req_json(url, params=None, headers=None):
    headers["Host"] = url.split("/")[2]
    r = requests.get(url, params=params, headers=headers)
    return json.loads(r.text)


def get_req_content(url, params=None, headers=None):
    headers["Host"] = url.split("/")[2]
    r = requests.get(url, params=params, headers=headers)
    return r.content


def get_req_text(url, params=None, headers=None):
    headers["Host"] = url.split("/")[2]
    r = requests.get(url, params=params, headers=headers)
    return r.text


def python_list2_web_list(data):
    web_list = "[\""
    web_list += '", "'.join(data)
    web_list += "\"]"
    return web_list




#utis API

import json
from urllib.parse import urlparse, parse_qs, urlencode

def parse_query(url):
    result = urlparse(url)
    query = result.query
    query_dict = parse_qs(query)
    query_dict = {k: v[0] for k, v in query_dict.items()}
    return query_dict

def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response

def set_url(domain, _dict):
    path = urlencode(_dict)
    url = domain + '?%s' % path
    return url

def get_param_url(_dict):
    return urlencode(_dict)

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

def get_tt_param(text):
    password = 'webapp1.0+202106'
    text = text + '&is_encryption=1'
    print('''code by t.me/toolav''')
    iv = password.encode()
    password = password.encode()
    msg = pad(text.encode(), AES.block_size)
    cipher = AES.new(password, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(msg)
    out = b64encode(cipher_text).decode('utf-8')
    return out
