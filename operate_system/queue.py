#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time :2020/4/12 16:57


import time
import threading


class ThreadSafeQueueException(Exception):
    pass


# 线程安全的队列
class ThreadSafeQueue(object):

    def __init__(self, max_size=0):
        self.queue = []
        self.max_size = max_size
        self.lock = threading.Lock()
        self.condition = threading.Condition()

    # 当前队列元素的数量
    def size(self):
        self.lock.acquire()
        size = len(self.queue)
        self.lock.release()
        return size

    # 往队列里放入元素
    def put(self, item):
        if self.max_size != 0 and self.size() > self.max_size:
            return ThreadSafeQueueException()

        self.lock.acquire()
        self.queue.append(item)
        self.lock.release()
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()

    def batch_put(self, item_list):
        if not isinstance(item_list, list):
            item_list = list(item_list)

        for item in item_list:
            self.put(item)

    # 从队列里取
    def pop(self, block=True, timeout=None):
        if self.size() == 0:
            if block:
                self.condition.acquire()
                self.condition.wait(timeout=timeout)
                self.condition.release()

            else:
                return None

        self.lock.acquire()
        item = None
        if len(self.queue) > 0:
            item = self.queue.pop()

        self.lock.release()
        return item

    def get(self, index):
        self.lock.acquire()
        item = self.queue[index]
        self.lock.release()
        return item


if __name__ == '__main__':
    queue = ThreadSafeQueue(max_size=100)

    def producer():
        while True:
            queue.put(1)
            time.sleep(3)

    def consumer():
        while True:
            item = queue.pop(block=True, timeout=5)
            print("get item from queue: {}".format(item))
            time.sleep(1)

    thd1 = threading.Thread(target=producer)
    thd2 = threading.Thread(target=consumer)

    thd1.start()
    thd2.start()
    thd1.join()
    thd2.join()