#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__:JasonLIN
import os
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_PATH = os.path.join(BASE_PATH, "db", "user")

TRANSACTION_TYPE = {
    'pay': {'action': "+", "interest": 0},
    'repay': {'action': '+', 'interest': 0},
    'withdraw': {'action': '-', 'interest': 0.05},
    'transfer': {'action': '-', 'interest': 0.05},
    'receive': {'action': '+', 'interest': 0},

}

LOG_TYPES = {
    'transaction': 'transactions.log',
    'access': 'access.log',
}

TRANS_LOG_PATH = os.path.join(BASE_PATH, "log", "transactions.log")