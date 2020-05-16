#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time :2020/4/12 17:43

import time

from operate_system import task, pool


class SimpleTask(task.Task):
    def __init__(self, callable):
        super(SimpleTask, self).__init__(callable)


def process():
    time.sleep(1)
    print('This is a SimpleTask callable function1')
    time.sleep(1)
    print('This is a SimpleTask callable function2')


def test():
    test_pool = pool.ThreadPool()
    test_pool.start()

    for i in range(10):
        simple_task = SimpleTask(process)
        test_pool.put(simple_task)


# 测试异步任务
def test_async_task():

    def async_process():
        num = 0
        for i in range(100):
            num += i
        return num

    test_pool = pool.ThreadPool()
    test_pool.start()

    for i in range(10):
        async_task = task.AsyncTask(func=async_process)
        test_pool.put(async_task)
        result = async_task.get_result()
        print("Get result: %d" % result)


# 测试是否可以正在的等待(wait)
def test_async_task2():

    def async_process():
        num =0
        for i in range(100):
            num += i
        time.sleep(5)
        return num

    test_pool = pool.ThreadPool()
    test_pool.start()

    for i in range(10):
        async_task = task.AsyncTask(func=async_process)
        test_pool.put(async_task)
        print("Put Task: %d" % time.time())
        result = async_task.get_result()
        print("Get result: %d; time: %d" % (result, time.time()))


# 测试没有等待是否正常(wait)
def test_async_task3():

    def async_process():
        num =0
        for i in range(100):
            num += i
        return num

    test_pool = pool.ThreadPool()
    test_pool.start()

    for i in range(10):
        async_task = task.AsyncTask(func=async_process)
        test_pool.put(async_task)
        print("Put Task: %d" % time.time())
        result = async_task.get_result()
        print("Get result: %d; time: %d" % (result, time.time()))


if __name__ == '__main__':
    # test()
    # test_async_task()
    # test_async_task2()
    test_async_task3()