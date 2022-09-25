#!/usr/bin/env python3
try:
    import requests
    for port in range(10000, 65535):
        try:
            print('{} on port {}'.format(requests.get('http://localhost:{}'.format(port)), port))
        except Exception as e:
            print("{}: {}".format(type(e).__name__, port), end="\r")
except KeyboardInterrupt:
    print(' \nInterrupted! ')
