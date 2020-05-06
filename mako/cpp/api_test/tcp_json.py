#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import socket

req = {}
req['type'] = 0x1002
req['user_id'] = 'uid122113'

req = json.dumps(req)

# j = json.loads(req)
req = "%08s%s" % (len(req), req)
req = req.encode()

# tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# tcp_client.connect(("127.0.0.1", 12345))
# print(req)

count = 10000
while count > 0:
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.connect(("127.0.0.1", 12345))
    sb = tcp_client.send(req)
    # print("send byte:", sb)
    resp = tcp_client.recv(1000)
    count = count - 1
    # print(resp.decode(encoding="utf8"))
