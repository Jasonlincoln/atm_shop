#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__:JasonLIN
import logging
from atm.bank.conf import settings


def my_log(log_type):
    logger = logging.getLogger(log_type)  # 定义Logger的名字
    logger.setLevel(logging.INFO)  # 低于这个级别将被忽略，后面还可以设置输出级别

    # 创建handler和输出级别
    ch = logging.StreamHandler()  # 输出到屏幕
    ch.setLevel(logging.ERROR)  # 输出级别

    # 创建日志格式，可以为每个handler创建不同的格式
    log_file = "%s/log/%s" % (settings.BASE_PATH, settings.LOG_TYPES[log_type])
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch and fh
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch and fh to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger


trans_log = my_log("transaction")
access_log = my_log("access")
