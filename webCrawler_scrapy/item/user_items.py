# -*- coding: utf-8 -*-
# @Time    : 2019/02/24 16:21
# @Author  : Hanrd
# @File    : user_items.py
# @Software: PyCharm

import scrapy


class UserScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    user_id = scrapy.Field()  # 用户id
    user_name = scrapy.Field()  # 用户名
    user_sex = scrapy.Field()  # 性别
    user_regtime = scrapy.Field()  # 注册时间
    user_area = scrapy.Field()  # 地区
    user_pid = scrapy.Field()  # 省份id
    user_cid = scrapy.Field()  # 城市id
    user_pname = scrapy.Field()  # 省份
    user_cname = scrapy.Field()  # 城市
    user_carname = scrapy.Field()  # 用户车名称

