#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time :2020/4/12 18:22


import struct
import socket


# IP报文解析器
class IPParser:

    IP_HEADER_LENGTH = 20

    @classmethod
    def parser_ip_header(cls, ip_header):
        """
        IP报文格式
        1. 4位Ip-version 4位IP头长度，服务类型， 16位总长度
        2. 16位标识符 3位标记位 3位片偏移
        3. 8位TTL 8位协议 16位IP头校验和
        4. 32位源IP地址
        5. 32位目的IP地址
        :param ip_header:
        :return:
        """
        line1 = struct.unpack('>BBH', ip_header[:4])
        # eg 11110000 => 1111
        ip_version = line1[0] >> 4

        iph_length = line1[0] & 15 * 4
        pkg_length = line1[2]

        line3 = struct.unpack('>BBH', ip_header[8:12])
        TTL = line3[0]
        protocol = line3[1]
        iph_checksum = line3[2]

        line4 = struct.unpack(">4s", ip_header[12:16])
        src_ip = socket.inet_ntoa(line4[0])

        line5 = struct.unpack('>4s', ip_header[16:20])
        dst_ip = socket.inet_ntoa(line5[0])

        return {
            "ip_version": ip_version,
            "iph_length": iph_length,
            "pkg_length": pkg_length,
            "TTL": TTL,
            "protocol": protocol,
            "iph_checksum": iph_checksum,
            "src_ip": src_ip,
            "dst_ip": dst_ip
        }

    @classmethod
    def parse(cls, packet):
        ip_header = packet[:20]
        return cls.parser_ip_header(ip_header)