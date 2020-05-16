#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time :2020/3/24 21:29

import socket


def client(i):
    s = socket.socket()
    s.connect(("127.0.0.1", 6666))
    print("recv msg %s %d" % (s.recv(1024), i))
    s.close()


if __name__ == '__main__':
    for i in range(10):
        client(i)