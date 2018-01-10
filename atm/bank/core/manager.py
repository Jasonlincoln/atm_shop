#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__:JasonLIN
import configparser
from atm.bank.conf import settings
config = configparser.ConfigParser()
user_path = settings.USER_PATH
config.read(user_path)
user_list = config.sections()


def add():
    while True:
        print("-------后台管理--------")
        username = input("用户名>>").strip()
        if username in user_list:
            print("用户名已经存在，不可重复创建")
            continue
        elif username == "q":
            return
        else:
            password = input("密码>>").strip()
            credit = input("额度>>").strip()
            try:
                config.add_section(username)
                config.set(username, "username", username)
                config.set(username, "password", password)
                config.set(username, "credit", credit)
                config.set(username, "balance", credit)
                config.set(username, "lock", "0")
                config.write(open(user_path, "w"))
                print("创建用户【%s】成功，额度为【%.2f】" % (username, float(credit)))
                return
            except Exception as e:
                print(e)


def update_pwd(user):
    new_pwd = input("新密码>>").strip()
    config.set(user, "password", new_pwd)
    print("修改密码成功，新密码【%s】" % new_pwd)
    config.write(open(user_path, "w"))


def update_credit(user):
    new_credit = input("额度>>").strip()
    config.set(user, "credit", new_credit)
    print("额度修改为【%s】" % new_credit)
    config.write(open(user_path, "w"))


def update_lock(user):
    choice = input("锁定/解锁用户Y/N?".strip())
    if choice == "Y":
        config.set(user, "lock", "1")
        print("【%s】账号已经锁定!" % user)
    elif choice == "N":
        config.set(user, "lock", "0")
        print("【%s】账号已经解锁！" % user)
    else:
        print("输入有误")
        return
    config.write(open(user_path, "w"))


def update():
    for k, v in enumerate(user_list):
        print(k, v)
    choice = input("选择用户>>").strip()
    if len(choice) == 0:
        return
    user = user_list[int(choice)]
    print("choice", user)
    dic = {"1": update_pwd,
           "2": update_credit,
           "3": update_lock
           }
    cmd_info = """
    1 --> 更改密码，
    2 --> 更改额度，
    3 --> 锁定/解锁
    """.format()
    print(cmd_info)
    cmd = input("cmd>>").strip()
    try:
        dic[cmd](user)
        return
    except Exception:
        print("输入有误")
  
    
def run():
    func_dic = {"1": add,
                "2": update}
    info = """
    1 --> 添加用户
    2 --> 更新用户信息
    """.format()
    while True:
        print(info)
        cmd = input(">>").strip()
        if cmd in func_dic:
            func_dic[cmd]()
        elif cmd == "q":
            break
        else:
            print("输入有误")