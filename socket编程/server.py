#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time :2020/3/24 21:26

import socket

def server():
    s = socket.socket()
    host = '127.0.0.1'
    port = 6666
    s.bind((host, port))
    s.listen(5)

    while True:
        c, addr = s.accept()
        print("conect", addr)
        c.send(b"welcome")
        c.close()


if __name__ == '__main__':
    server()