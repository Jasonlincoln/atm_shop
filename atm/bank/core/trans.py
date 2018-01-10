#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__:JasonLIN

import configparser
from atm.bank.conf import settings
config = configparser.ConfigParser()
user_path = settings.USER_PATH
config.read(user_path)
trans_dic = settings.TRANSACTION_TYPE


def transaction(user, func, amount):
    """交易处理函数"""
    amount = float(amount)
    trans_type = trans_dic[func]["action"]
    interest_rates = trans_dic[func]["interest"]
    interest = float(interest_rates) * amount
    balance = float(config.get(user, "balance"))
    try:
        if trans_type == "+":
            new_balance = balance + amount + interest
        elif trans_type == "-":
            if balance > amount:
                new_balance = balance - amount - interest
            else:
                print("\033[31;1m余额不足，只剩[%d]\033[0m" % balance)
                return
        else:
            return
        config.set(user, "balance", str(new_balance))
        config.write(open(user_path, 'w'))
        return new_balance
    except Exception as e:
        print(e)


        