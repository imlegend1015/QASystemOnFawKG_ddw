# -*- coding: utf-8 -*-
# @Time    : 2019/02/24 16:58
# @Author  : Hanrd
# @File    : auto_home_users.py
# @Software: PyCharm

import scrapy
import copy
import json
import re
from webCrawler_scrapy.lib.util import check_json_format
from webCrawler_scrapy.item.user_items import UserScrapyItem

class AutoHomeUsersSpider(scrapy.spiders.Spider):
    name = "users"
    allowed_domains = ["mobile.app.autohome.com.cn"]
    start_urls = ["http://mobile.app.autohome.com.cn/user_v7.0.0/User/GetUserInfo.ashx?tid=11967537"]
    user_id = 11967537

    def parse(self, response):
        item = UserScrapyItem()
        yield scrapy.Request(url=response.url, callback=self.parse_user_items, meta={"item": copy.deepcopy(item)})

    def parse_user_items(self, response):
        self.user_id += 1
        item = response.meta['item']
        content = response.body.decode()
        if check_json_format(content):
            content = json.loads(content)
        else:
            content = re.sub('"title":".{6,30}",', '"title":" ",', content)
            content = json.loads(content)
        if "无结果集" not in content["message"] or "GetInfoFromUserCenter(int userId) is null" not in content["message"]:
            result = content["result"]
            item["user_id"] = result["userid"]
            item["user_name"] = result["name"]
            item["user_sex"] = result["sex"]
            item["user_carname"] = result["mycarname"]
            item["user_regtime"] = result["regtime"]
            item["user_pid"] = result["provinceid"]
            item["user_pname"] = result["provincename"]
            item["user_cid"] = result["cityid"]
            item["user_cname"] = result["cityname"]
            item["user_area"] = result["areaname"]
            yield item
        if self.user_id <= 100000000:
            base_url = "http://mobile.app.autohome.com.cn/user_v7.0.0/User/GetUserInfo.ashx?tid=%s"
            url = base_url % self.user_id
            yield scrapy.Request(url=url, callback=self.parse_user_items, meta={"item": copy.deepcopy(item)})
