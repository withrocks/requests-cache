#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

import requests
import requests_cache
import logging

logging.basicConfig(level=logging.DEBUG)


"""
def main():
    # Once cached, delayed page will be taken from cache
    # redirects also handled
    for i in range(5):
        requests.get('http://httpbin.org/delay/1')
        r = requests.get('http://httpbin.org/redirect/1')
        print(r.text)

    # And if we need to get fresh page or don't want to cache it?
    with requests_cache.disabled():
        print(requests.get('http://httpbin.org/ip').text)

    # Debugging info about cache
    print(requests_cache.get_cache())
"""
def main():
    print(requests.get('http://httpbin.org/ip').text)


if __name__ == "__main__":
    requests_cache.install_cache('example_cache', backend="file")
    t = time.time()
    main()
    print('Elapsed: %.3f seconds' % (time.time() - t))
