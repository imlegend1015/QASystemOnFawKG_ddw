# -*- coding: utf-8 -*-
# @Time    : 2019/02/24 17:09
# @Author  : Hanrd
# @File    : util.py
# @Software: PyCharm
import json


def check_json_format(raw_msg):
    """
    用于判断一个字符串是否符合json格式
    """
    if isinstance(raw_msg, str):  # 首先判断变量是否为字符串
        try:
            json.loads(raw_msg, encoding='utf-8')
        except ValueError:
            return False
        return True
    else:
        return False
