#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__:JasonLIN
import sys
# print(sys.path)
import configparser
from atm.bank.conf import settings
from atm.bank.core import manager
from atm.bank.core.log import access_log
config = configparser.ConfigParser()
user_path = settings.USER_PATH
config.read(user_path)
login_tag = 0


def authentic(func):
    def inner(*args):
        # print(">>>", args, func)
        if login_tag == 0:
            login()
        elif login_tag == 1:
            func(args[0])
    return inner


def login():
    """
    atm登录，输入用户名，密码

    """
    i = 0
    j = 0
    while True:
        username = input("用户名>>").strip()
        if username == "q":
            exit("正在退出".center(50, "-"))
        user_list = config.sections()
        if i == 2:  # 用户名错误太多
            return
        elif j == 2:  # 用户名或者密码错误太多
            config.set(username, "lock", "1")
            config.write(open("user", "w"))
            print("错误次数太多")
            access_log.info("【%s】输入密码错误次数3次" % username)
            return
        elif username not in user_list:
            access_log.info("【%s】用户名不存在" % username)
            print("用户名不存在")
            i += 1
            continue
        else:  # 如果用户存在
            password = input("密码>>").strip()
            if config.get(username, "lock") == "1":
                print("\033[31;1m用户[%s]已经被锁定，请联系管理员\033[0m")
                access_log.info("\【%s】账号被锁定，登录失败" % username)
                continue
            user = config.get(username, "username")
            pwd = config.get(username, "password")
            if user == username and pwd == password:
                global login_tag
                login_tag = 1
                if user == "admin":
                    access_log.info("管理员登录")
                    manager.run()
                    return
                print("welcome %s".center(50, "-") % username)
                access_log.info("【%s】登录成功" % user)
                return user
            else:
                print("密码不正确，重新输入")
                access_log.info("【%s】第%d登录失败" % (username, int(j+1)))
                j += 1


    
    
    