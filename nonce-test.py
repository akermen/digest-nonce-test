# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#
# nonce-test.py
#
# Created by Ahmet Kermen on 14.01.2022.
#
#------------------------------------------------------------------------------
import sys
import requests
import time
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
#------------------------------------------------------------------------------
request_count = 3
worker_count = 3
#------------------------------------------------------------------------------
second = len(sys.argv) == 2 and sys.argv[1] == 'second'
#------------------------------------------------------------------------------
host = 'http://127.0.0.1:8080'
username = 'testuser'
password = 'testpass'
#------------------------------------------------------------------------------
def auth_request(index):

    if second:
        # exactly 1 second between each request to see nonce resolution
        time.sleep(1.0 * (index -1))

    res = requests.get(host)
    if res.status_code == 401:
        k = 'WWW-Authenticate'
        h = res.headers[k]
        for k in h.split(','):
            (a, b) = k.split('=')
            if a.rstrip().lstrip() == 'nonce':
                print('request: %s nonce: %s' % (index, b))
#------------------------------------------------------------------------------
def main():
    with PoolExecutor(max_workers=worker_count) as executor:
        for _ in executor.map(auth_request, range(1, request_count +1)):
            pass
#------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
#------------------------------------------------------------------------------
