#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__:JasonLIN
import configparser
import os
import re
import sys
from atm.bank.conf import settings
from atm.bank.core import auth
from atm.bank.core import trans
from atm.bank.core.log import trans_log
config = configparser.ConfigParser()
user_path = settings.USER_PATH
config.read(user_path)


@auth.authentic
def withdraw(user):
    """取款"""
    while True:
        amount = input("金额>>").strip()
        if amount.isdigit():
            res = trans.transaction(user, "withdraw", amount)
            if res:
                print("\033[32;1m【%s】取款【%.2f】,余额【%.2f】\033[0m"
                      % (user, float(amount), float(res)))
                trans_log.info("account: %s  trans_type: withdraw amount: %.2f "
                               % (user, float(amount)))
                return
        elif amount == "q":
            return
        else:
            print("请输入数字")
 

@auth.authentic
def transfer(user):
    while True:
        tran_id = input("转账用户名>>").strip()
        user_list = config.sections()
        if tran_id in user_list:
            while True:
                amount = input("转账金额>>").strip()
                if amount.isdigit():
                    new_balance = trans.transaction(user, "transfer", amount)
                    trans.transaction(tran_id, "receive", amount)
                    trans_log.info("account: %s trans_type: receive amount: %s"
                                   % (tran_id, float(amount)))
                    if new_balance:
                        print("\033[32;1m【%s】转账给【%s】，金额为【%2.f】余额为【%2.f】\033[0m"
                              % (user, tran_id, float(amount), float(new_balance)))
                        trans_log.info("account: %s，trans_type: transfer amount: %2.f "
                                       % (user, float(amount),))
                        return
                elif amount == "q":
                    return
                else:
                    print("请输入数字")
        elif tran_id == "q":
            return
        else:
            print("用户名不存在，重新输入")
            
            
@auth.authentic
def repay(user):
    """还款"""
    amount = input("还款金额>>").strip()
    if amount.isdigit():
        res = trans.transaction(user, "repay", amount)
        if res:
            print("\033[32;1m【%s】还款【%2.f】成功，余额【%2.f】\033[0m"
                  % (user, float(amount), float(res)))
            trans_log.info("account: %s amount: %.2f"
                           % (user, float(amount)))
    else:
        print("请输入数字")

       
def pay_api(pay_amount):
    """付款,对外接口
    user: 用户名
    pay_amount: 付款金额
    """
    print("---------welcome bank--------")
    user = auth.login()
    new_balance = trans.transaction(user, "pay", pay_amount)
    if new_balance:
        trans_log.info("account: %s pay amount: %.2f" % (user, float(pay_amount)))
    return new_balance


@auth.authentic
def pay_check(user):
    with open(settings.TRANS_LOG_PATH, "r", encoding="gbk") as f:
        for line in f:
            if re.search("account: %s" % user, line):
                print(line)
            
            
def atm_exit(user):
    info = ("""
******再见【%s】*******

     欢迎下次光临
     
*********************
""".format() % user)
    print(info)


def run():
    """主函数，程序入口"""
    cmd_dic = {
        "1": transfer,
        "2": repay,
        "3": pay_check,
        "4": withdraw,
        "6": atm_exit,
        "7": pay_api,
    }
    info = """
-----------ATM-----------
        1 --> 转账
        2 --> 还款
        3 --> 查询账单
        4 --> 取款
        6 --> 退出
-------------------------
        """.format()
    user = auth.login()
    while True:
        # print("user", user)
        print(info)
        cmd = input(">>").strip()
        if cmd in cmd_dic:
            cmd_dic[cmd](user)
        else:
            print("输入有误，重新输入")

