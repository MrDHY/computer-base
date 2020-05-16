#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time :2020/4/12 18:05
"""
帮助理解struct数据，大小端数据, C语言结构体数据转为python的数据
"""

import struct

# 八个字节
bin_str = b'ABCD1234'
print(bin_str)
result = struct.unpack('>BBBBBBBB', bin_str)
print(result)
result = struct.unpack('>HHHH', bin_str)
print(result)
result = struct.unpack('>LL', bin_str)
print(result)
result = struct.unpack('>8s', bin_str)
print(result)
result = struct.unpack('>BBHL', bin_str)
print(result)