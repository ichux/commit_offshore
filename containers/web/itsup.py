#!/usr/bin/env python3
import socket
import time
import os

PORT=16432

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', PORT))
        if result == 0:
            print(f"+ {PORT}")
            break
        else:
            print(f"- {PORT}")
            time.sleep(1)
