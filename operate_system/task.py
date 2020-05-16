#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time :2020/4/12 16:49

import uuid
import threading


# 基本任务
class Task:

    def __init__(self, func, *args, **kwargs):
        # 任务逻辑
        self.callable = func
        self.id = uuid.uuid4()
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return "Task id " + str(self.id)


# 异步任务对象
class AsyncTask(Task):

    def __init__(self, func, *args, **kwargs):
        super().__init__(func, *args, **kwargs)
        self.result = None
        self.condition = threading.Condition()

    def set_result(self, result):
        self.condition.acquire()
        self.result = result
        self.condition.notify()
        self.condition.release()

    def get_result(self):
        self.condition.acquire()
        if not self.result:
            self.condition.wait()
        result = self.result
        self.condition.release()
        return result


def my_function():
    print("Task test")


if __name__ == '__main__':
    task = Task(func=my_function)
    print(task)