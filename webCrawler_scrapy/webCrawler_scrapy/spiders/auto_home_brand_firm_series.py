# -*- coding: utf-8 -*-
# @Time    : 2019/02/24 14:45
# @Author  : Hanrd
# @File    : auto_home_brand_firm_series.py
# @Software: PyCharm
import json
# import time

import scrapy


from webCrawler_scrapy.item.brand_firm_series_items import BrandFirmSeriesItem

class AutoHomeBrandSpider(scrapy.spiders.Spider):
    name = "brands_firms_series"
    allowed_domains = ["cars.app.autohome.com.cn"]
    start_urls = ["https://cars.app.autohome.com.cn/cars_v9.1.0/cars/brands-pm1.json?pluginversion=9.9.5"]

    def parse(self, response):
        content = json.loads(response.body.decode())
        brand_list = content["result"]["brandlist"]
        for i in range(len(brand_list)):
            for j in range(len(brand_list[i]['list'])):
                item = BrandFirmSeriesItem()
                item["brand_name"] = brand_list[i]['list'][j]["name"]
                brand_id = brand_list[i]['list'][j]["id"]
                item["brand_id"] = brand_id
                url_1 = "https://cars.app.autohome.com.cn/cars_v9.1.0/cars/seriesprice-pm1-b" + str(brand_id) + \
                        "-t16-v9.9.5-c110100.json?pluginversion=9.9.5"
                yield scrapy.Request(url=url_1, callback=self.parse_1, meta={"item": item})

    def parse_1(self, response):
        content = json.loads(response.body.decode())
        item = response.meta['item']
        fct_list_1 = []
        fct_list = content['result']['fctlist']  # 在售
        for firm in fct_list:
            firm_dict = dict()
            firm_dict['firm'] = firm['name']

            series_list = []
            for series in firm['serieslist']:
                series_list_item = dict()
                series_list_item['series_id'] = series['id']
                series_list_item['series_name'] = series['name']
                series_list_item['level_id'] = series['levelid']
                series_list_item['level_name'] = series['levelname']
                series_list_item['price'] = series['price']
                series_list.append(series_list_item)
            firm_dict['serieslist'] = series_list

            fct_list_1.append(firm_dict)
        item['on_sale_list'] = fct_list_1

        fct_list_1 = []
        fct_list = content['result']['otherfctlist']  # 停售
        for firm in fct_list:
            firm_dict = dict()
            firm_dict['firm'] = firm['name']

            series_list = []
            for series in firm['serieslist']:
                if series['state'] == 40:
                    series_list_item = dict()
                    series_list_item['series_id'] = series['id']
                    series_list_item['series_name'] = series['name']
                    series_list_item['level_id'] = series['levelid']
                    series_list_item['level_name'] = series['levelname']
                    series_list_item['price'] = series['price']
                    series_list.append(series_list_item)
            firm_dict['serieslist'] = series_list

            fct_list_1.append(firm_dict)
        item['halt_sale_list'] = fct_list_1

        fct_list_1 = []
        fct_list = content['result']['otherfctlist']  # 未售
        for firm in fct_list:
            firm_dict = dict()
            firm_dict['firm'] = firm['name']

            series_list = []
            for series in firm['serieslist']:
                if series['state'] == 0:
                    series_list_item = dict()
                    series_list_item['series_id'] = series['id']
                    series_list_item['series_name'] = series['name']
                    series_list_item['level_id'] = series['levelid']
                    series_list_item['level_name'] = series['levelname']
                    series_list_item['price'] = series['price']
                    series_list.append(series_list_item)
            firm_dict['serieslist'] = series_list

            fct_list_1.append(firm_dict)
        item['for_sale_list'] = fct_list_1
        yield item
