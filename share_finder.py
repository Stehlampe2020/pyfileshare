#!/usr/bin/env python3
try:
    import requests
    for port in range(49152, 65535):
        try:
            print(f'{requests.get(f"http://localhost:{port}")} on port {port}', timeout=3)
        except Exception as e:
            print(f"{type(e).__name__}: {port}", end="\r")
except KeyboardInterrupt:
    print(' \nInterrupted! ')
