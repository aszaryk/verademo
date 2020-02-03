#!/usr/bin/env python3
import os
import time                                                                     
import hmac                                                                     
import codecs
import json  
import sys                                                              
from hashlib import sha256 
import requests
from requests.adapters import HTTPAdapter                                       
from urllib.parse import urlparse

#Setup variables according to environment

#Jenkins:
api_id = os.getenv("VeraID")
api_secret = os.getenv("VeraPW")
dynamic_job = os.getenv("JOB_NAME")


def veracode_hmac(host, url, method):
    signing_data = 'id={api_id}&host={host}&url={url}&method={method}'.format(
                    api_id=api_id.lower(),
                    host=host.lower(),
                    url=url, method=method.upper())

    timestamp = int(round(time.time() * 1000))
    nonce = os.urandom(16).hex()

    key_nonce = hmac.new(
        codecs.decode(api_secret, 'hex_codec'),
        codecs.decode(nonce, 'hex_codec'), sha256).digest()

    key_date = hmac.new(key_nonce, str(timestamp).encode(), sha256).digest()
    signature_key = hmac.new(
            key_date, 'vcode_request_version_1'.encode(), sha256).digest()
    signature = hmac.new(
            signature_key, signing_data.encode(), sha256).hexdigest()

    return '{auth} id={id},ts={ts},nonce={nonce},sig={sig}'.format(
            auth='VERACODE-HMAC-SHA-256',
            id=api_id,
            ts=timestamp,
            nonce=nonce,
            sig=signature)

def prepared_request(method, end_point, json=None, query=None, file=None):
    session = requests.Session()
    session.mount(end_point, HTTPAdapter(max_retries=3))
    request = requests.Request(method, end_point, json=json, params=query, files=file)
    prepared_request = request.prepare()
    prepared_request.headers['Authorization'] = veracode_hmac(
        urlparse(end_point).hostname, prepared_request.path_url, method)
    res = session.send(prepared_request)

    return res

# code above this line is reusable for all/most API calls

#Payload for creating and scheduling new DA job
data =   {
  "name": dynamic_job,
  "scans": [
    {
      "scan_config_request": {
        "target_url": {
          "url": "http://my.staging.site"
        }
      }
    }
  ],
  "schedule": {
    "now": True,
    "duration": {
      "length": 1,
      "unit": "DAY"
    }
  }
}


print("Creating a new Dynamic Analysis Job: " + dynamic_job )
res = prepared_request('POST', 'https://api.veracode.com/was/configservice/v1/analyses', json=data)

if res.status_code == 201:
    print("Job Created and Submitted Successfully: " + str(res.status_code)
else:
    response = res.json()
    print("Error encountered: " + response['_embedded']['errors'][0]['detail'])