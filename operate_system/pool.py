#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time :2020/4/12 17:


import psutil
import threading

from operate_system.task import Task, AsyncTask
from operate_system.queue import ThreadSafeQueue


# 任务类型异常
class TaskTypeErrorException(Exception):
    pass


# 任务处理线程
class ProcessThread(threading.Thread):

    def __init__(self, task_queue,*args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        # 线程通知
        self.dismiss_flag = threading.Event()
        self.task_queue = task_queue
        self.args = args
        self.kwargs = kwargs

    def run(self):
        while True:
            if self.dismiss_flag.isSet():
                break

            task = self.task_queue.pop()
            if not isinstance(task, Task):
                continue

            # 执行task实际逻辑（是通过函数调用引进来的）
            result = task.callable(*task.args, **task.kwargs)
            if isinstance(task, AsyncTask):
                task.set_result(result)

    def dismiss(self):
        self.dismiss_flag.set()

    def stop(self):
        self.dismiss()


# 线程池
class ThreadPool:

    def __init__(self, size=10):
        if not size:
            # 约定线程池的大小为CPU核数的2倍
            size = psutil.cpu_count() * 2

        # 安全线程池
        self.pool = ThreadSafeQueue(size)
        # 安全任务池
        self.task_queue = ThreadSafeQueue()

        for i in range(size):
            self.pool.put(ProcessThread(self.task_queue))

    # 启动线程
    def start(self):
        for i in range(self.pool.size()):
            thd = self.pool.get(i)
            thd.start()

    # 停止线程
    def join(self):
        for i in range(self.pool.size()):
            thd = self.pool.get(i)
            thd.stop()

        while self.pool.size():
            thd = self.pool.pop()
            thd.join()

    # 往线程池提交任务
    def put(self, item):
        if not isinstance(item, Task):
            raise TaskTypeErrorException()
        self.task_queue.put(item)

    def batch_put(self, item_list):
        if not isinstance(item_list, list):
            item_list = list(item_list)

        for item in item_list:
            self.put(item)

    def size(self):
        return self.pool.size()