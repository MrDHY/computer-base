#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time :2020/4/12 18:04

import json
import socket

from operate_system.pool import ThreadPool as tp
from operate_system.task import AsyncTask

from computer_network.processor.net.parser import IPParser
from computer_network.processor.trans.parser import UDPParser, TCPParser


class ProcessTask(AsyncTask):

    def __init__(self, packet, *args, **kwargs):
        self.packet = packet
        super().__init__(func=self.process, *args, **kwargs)


    def process(self):
        header = {
            'network_header': None,
            'transport_header': None
        }
        ipheader = IPParser.parser_ip_header(self.packet)
        # print(ipheader)
        header['network_header'] = ipheader
        if ipheader['protocol'] == 17:
            udp_header = UDPParser.parse(packet=self.packet)
            header['transport_header'] = udp_header
        elif ipheader['protocol'] == 6:
            tcp_header = TCPParser.parse(packet=self.packet)
            header['transport_header'] = tcp_header
        return header


class Server:

    def __init__(self):
        # 工作协议类型，套接字类型，工作具体协议
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                  socket.IPPROTO_IP)

        # 更换为自己的IP
        self.ip = '192.168.1.12'
        self.port = 8888
        self.sock.bind((self.ip, self.port))

        # 混杂模式
        self.sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        self.pool = tp(10)
        self.pool.start()

    # 启动服务
    def loop_server(self):
        while True:

            #1. 接受
            packet, addr = self.sock.recvfrom(65535)

            #2. 生成task
            task = ProcessTask(packet)

            #3. 提交
            self.pool.put(task)

            #4 获取结果
            result = task.get_result()
            result = json.dumps(result, indent=4)
            print(result)


if __name__ == '__main__':
    s = Server()
    s.loop_server()