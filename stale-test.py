# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#
# stale-test.py
#
# Created by Ahmet Kermen on 05.04.2025
#
#------------------------------------------------------------------------------
import sys
import requests
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from requests.auth import AuthBase
#------------------------------------------------------------------------------
request_count = 100
worker_count = 100
#------------------------------------------------------------------------------
second = len(sys.argv) == 2 and sys.argv[1] == 'second'
#------------------------------------------------------------------------------
host = 'http://127.0.0.1:8080/'
username = 'testuser'
password = 'testpass'
#------------------------------------------------------------------------------
class CustomAuth(AuthBase):
    def __init__(self, username, password, data):
        self.username = username
        self.password = password
        self.data = data

    def __call__(self, r):

        ha1 = hashlib.md5('{}:{}:{}'.format(self.username, self.data['Digest realm'], self.password).encode('utf-8')).hexdigest()
        ha2 = hashlib.md5('GET:/'.encode('utf-8')).hexdigest()

        nc = '00000001'
        cnonce = '0a4f113b'
        response = hashlib.md5('{}:{}:{}:{}:{}:{}'.format(ha1, self.data['nonce'], nc, cnonce, self.data['qop'], ha2).encode('utf-8')).hexdigest()

        authorization = 'Digest username="{}", realm="{}", nonce="{}", uri="/", qop={}, nc={}, cnonce="{}", response="{}", opaque="{}"'.format(
            self.username, self.data['Digest realm'], self.data['nonce'], self.data['qop'], nc, cnonce, response, self.data['opaque'])

        r.headers['Authorization'] = authorization
        return r
#------------------------------------------------------------------------------
def auth_request(index):

    HEADER_AUTH = 'WWW-Authenticate'

    if second:
        # exactly 1 second between each request to see nonce resolution
        time.sleep(1.0 * (index -1))

    res = requests.get(host)
    if res.status_code == 401 and HEADER_AUTH in res.headers:

        first_headers = res.headers
        header_auth = res.headers[HEADER_AUTH]

        auth_data = {
            "nonce": None,
            "Digest realm": None,
            "qop": None,
            "algorithm": None,
            "opaque": None,
        }

        for header_auth_item in header_auth.split(','):
            (header_auth_key, header_auth_value) = header_auth_item.split('=')
            for key in auth_data:
                if header_auth_key.rstrip().lstrip() == key:
                    auth_data[key] = header_auth_value.replace('"', '')


        auth = CustomAuth(username, password, auth_data)
        res = requests.get(host, auth=auth)
        if res.status_code == 200:
            pass
            # print('{}: √'.format(index))
        else:
            if res.status_code == 401 and HEADER_AUTH in res.headers:
                header_auth = res.headers[HEADER_AUTH]
                for header_auth_item in header_auth.split(','):
                    (header_auth_key, header_auth_value) = header_auth_item.split('=')
                    if header_auth_key.rstrip().lstrip() == 'stale':
                        # print('{}: stale: {}'.format(index, header_auth_value))
                        break
                else:
                    print('{}: {}'.format(index, first_headers))
                    print('{}: {}'.format(index, res.headers))
#------------------------------------------------------------------------------
def main():
    with PoolExecutor(max_workers=worker_count) as executor:
        for _ in executor.map(auth_request, range(1, request_count +1)):
            pass
#------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
#------------------------------------------------------------------------------
