#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__:JasonLIN
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__:JasonLIN
import configparser
import os
import time
import pickle
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from atm.bank.core import my_bank

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
user_path = os.path.join(BASE_DIR, "db", "user")
shopping_path = os.path.join(BASE_DIR, "db", "shopping_dic")
config = configparser.ConfigParser()
config.read(user_path)
goods = [{'name': 'iphone', 'price': 5888},
         {'name': 'mac pro', 'price': 21888},
         {'name': 'bike', 'price': 888},
         {'name': '美女', 'price': 800},
         {'name': '键盘', 'price': 666}]


def register():
    user = input("用户名>>").strip()
    user_list = config.sections()
    if user in user_list:
        print("用户名已经存在，不可重复创建")
        return
    password = input("密码>>").strip()
    config.add_section(user)
    config.set(user, "username", user)
    config.set(user, "password", password)
    config.write(open(user_path, "w"))
    print("创建用户%s成功-----" % user)


def login():
    i = 0
    while i < 3:
        username = input("用户名>>").strip()
        password = input("密码>>").strip()
        user_list = config.sections()
        if username not in user_list:
            print("用户不存在")
            i += 1
            continue
        user = config.get(username, "username")
        pwd = config.get(username, "password")
        if user == username and pwd == password:
            print("welcome %s".center(50, '-') % username)
            return username
        else:
            print("\033[1;31m用户名或者密码不正确\033[0m")
            i += 1
            
    else:
        print("\033[1;31m密码错误次数太多\033[0m")


def save(username, good):
    """保存购买商品信息并记录时间"""
    buy_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    dic = {username: [{good: buy_time}]}
    with open(shopping_path, "rb") as f:
        shopping_dic = pickle.load(f)
    if shopping_dic.get(username):  # 已经买过
        shopping_list = shopping_dic[username]
        # {"jack":[{'bike': '2017-12-20 13:57:46'}, {'美女': '2017-12-20 13:57:47'}]}
        shopping_list.extend(dic[username])
        shopping_dic[username] = shopping_list
    else:  # 第一次买
        shopping_dic.update(dic)
    with open(shopping_path, "wb") as f:
        f.write(pickle.dumps(shopping_dic))  # 保存购买记录
    config.write(open(user_path, "w"))  # 更新余额


def show_record(username):
    """打印购买记录 """
    shopping_list = get_shopping_list(username)
    # [{"mac": "2017-12-20 21:14:23"}, {"iphone": "2017-12-20 21:15:45"}]
    for i in shopping_list:
        for j in i:
            print("%s购买了\033[1;32m[%s]\033[0m, 时间[%s]" % (username, j, i[j]))


def get_shopping_list(username):
    with open(shopping_path, "rb") as f:
        shopping_dic = pickle.load(f)
    shopping_list = shopping_dic[username]
    return shopping_list

def if_buy(username):
    with open(shopping_path, "rb") as f:
        shoppping_dic = pickle.load(f)
    if shoppping_dic.get(username):
        return 1

def show(username):
    with open(shopping_path, "rb") as f:
        shoppping_dic = pickle.load(f)
    if shoppping_dic.get(username):
        shopping_list = get_shopping_list(username)
        goods = []
        for i in shopping_list:
            for j in i:
                goods.append(j)
        info = """
    ---------%s----------
        用户名：%s
        已购商品：\033[1;32m%s\033[0m
    ---------------------
        """ % (username, username, goods)
        print(info)
        return


if __name__ == '__main__':
    info = """
-------shop------
    1 ---> 注册
    2 ---> 登录
-----------------
    """.format()
    while True:
        print(info)
        dic = {"1": register,
               "2": login, }
        choice = input(">>").strip()
        if choice == "exit":
            exit()
        if choice in dic:
            username = dic[choice]()
            if username:
                tag = if_buy(username)  # 又返回代表有购物记录
                if tag:
                    inquire = input("是否需要查询消费记录?[Y/N]")
                    if inquire == "Y":
                        show_record(username)
                while True:
                    print("================================")
                    for k, v in enumerate(goods):
                        print(k, "\033[1;32m[%s]\033[0m,price\033[1;32m[%s]\033[0m" % (v["name"], v["price"]))
                    choice = input("请输入商品序号>>").strip()
                    if choice == "exit":
                        show(username)
                        exit()
                    try:
                        good_dic = goods[int(choice)]
                        price = int(good_dic["price"])
                        balance = my_bank.pay_api(price)
                        if balance:
                            print("\033[1;31m%s已加入购物车\033[0m" % good_dic["name"])
                            save(username, good_dic["name"])
                        data = input("是否继续购物?[Y/N]").strip()
                        if data != "Y":  # 如果输入Y，继续购物
                            show(username)
                            exit()
                    except Exception as e:
                        print(e)
                        print("\033[1;31m输入序号有误\033[0m")
