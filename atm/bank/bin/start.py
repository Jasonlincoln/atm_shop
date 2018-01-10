#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__:JasonLIN
import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BASE_PATH)
sys.path.append(BASE_PATH)
from atm.bank.core import my_bank


if __name__ == '__main__':
    my_bank.run()