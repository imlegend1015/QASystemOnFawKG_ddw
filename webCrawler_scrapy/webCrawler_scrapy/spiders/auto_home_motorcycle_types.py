# -*- coding: utf-8 -*-
# @Time    : 2019/02/25 20:45
# @Author  : Hanrd
# @File    : auto_home_motorcycle_types.py
# @Software: PyCharm
import json
# import time

import scrapy


from webCrawler_scrapy.item.motorcycle_type_items import MotorcycleTypeItem

class AutoHomeBrandSpider(scrapy.spiders.Spider):
    name = "motorcycle"
    allowed_domains = ["cars.app.autohome.com.cn"]
    start_urls = ["https://cars.app.autohome.com.cn/cars_v9.1.0/cars/brands-pm1.json?pluginversion=9.9.5"]

    def parse(self, response):
        content = json.loads(response.body.decode())
        brand_list = content["result"]["brandlist"]
        for i in range(len(brand_list)):
            for j in range(len(brand_list[i]['list'])):
                brand_id = brand_list[i]['list'][j]["id"]  # 获取品牌id，跳转到品牌车系界面
                url_1 = "https://cars.app.autohome.com.cn/cars_v9.1.0/cars/seriesprice-pm1-b" + str(brand_id) + \
                        "-t16-v9.9.5-c110100.json?pluginversion=9.9.5"
                yield scrapy.Request(url=url_1, callback=self.parse_1)

    def parse_1(self, response):
        content = json.loads(response.body.decode())
        fct_list = content['result']['fctlist']  # 在售
        for firm in fct_list:
            for series in firm['serieslist']:
                series_id = series['id']  # 获取车系id，跳转到车系内的车型列表
                state = series['state']  # 20 在售 | 40 停售 | 0 未售
                url_2 = "https://cars.app.autohome.com.cn/carbase/seriessummary/carsbaseinfo?pm=1&seriesid=" \
                        + str(series_id) + "&cityid=110100&pluginversion=9.9.5"
                yield scrapy.Request(url=url_2, callback=self.parse_2, meta={'state': state})
        other_fct_list = content['result']['otherfctlist']  # 停售/未售
        for firm in other_fct_list:
            for series in firm['serieslist']:
                series_id = series['id']  # 获取车系id，跳转到车系内的车型列表
                state = series['state']  # 20 在售 | 40 停售 | 0 未售
                url_2 = "https://cars.app.autohome.com.cn/carbase/seriessummary/carsbaseinfo?pm=1&seriesid=" \
                        + str(series_id) + "&cityid=110100&pluginversion=9.9.5"
                yield scrapy.Request(url=url_2, callback=self.parse_2, meta={'state': state})

    def parse_2(self, response):
        state = response.meta['state']
        content = json.loads(response.body.decode())
        # 获取品牌车系信息
        series_info = content['result']['seriesbaseinfo']
        brand_id = series_info['brandid']
        brand_name = series_info['brandname']
        series_id = series_info['seriesid']
        series_name = series_info['seriesname']
        level_id = series_info['levelid']
        level_name = series_info['levelname']
        series_tags = series_info['seriestag']
        # 获取车型基本信息
        if len(content['result']['specinfo']['staticspeclist']) == 0:
            return
        spec_info = content['result']['specinfo']['staticspeclist'][0]
        if state == 20:
            on_sale = '在售'
        elif state == 40:
            on_sale = '停售'
        elif state == 0:
            on_sale = '未售'
        else:
            on_sale = ''  # 不可能出现
        spec_list = spec_info['yearspeclist']
        for elem in spec_list:
            category = elem['name']
            for elem_1 in elem['speclist']:
                item = MotorcycleTypeItem()
                # item['logo'] = logo
                item['brand_id'] = brand_id
                item['brand_name'] = brand_name
                item['series_id'] = series_id
                item['series_name'] = series_name
                item['level_id'] = level_id
                item['level_name'] = level_name
                item['series_tags'] = series_tags
                item['category'] = category
                item['on_sale'] = on_sale
                motorcycle_type_id = elem_1['id']
                item['motorcycle_type_id'] = motorcycle_type_id
                item['motorcycle_type_name'] = elem_1['name']
                item['recom_price'] = elem_1['price']
                item['description'] = elem_1['description']
                # 跳转到车型配置信息界面 获取配置信息
                url_3 = "https://cars.app.autohome.com.cn/cfg_v8.5.0/cars/newspeccompare.ashx?specids=" + \
                        str(motorcycle_type_id) + "&seriesid=0" + \
                        "&cityid=110100&pm=1&site=2&version=9.9.5&pluginversion=9.9.5"

                yield scrapy.Request(url=url_3, callback=self.parse_3, meta={"item": item})

    def parse_3(self, response):
        item = response.meta['item']
        content = json.loads(response.body.decode())
        param_0 = content['result']['paramitems']
        param_1 = content['result']['configitems']
        param_2 = content['result']['selectconfig']  # 选装包信息
        for sub_param in param_0:
            item_type = sub_param['itemtype']
            param_of_this_type = dict()
            for sub_item in sub_param['items']:
                name = sub_item['name']
                # if name == '车内PM2.5过滤装置':
                #     name = '车内PM过滤装置'
                value = sub_item['modelexcessids'][0]['value']  # 特殊处理几个符号
                if value == '●':
                    value = '标配'
                if value == '○':
                    value = '选配'
                if value == '-':
                    if 'sublist' in sub_item['modelexcessids'][0].keys():  # 是否有值
                        if len(sub_item['modelexcessids'][0]['sublist']) == 1:  # 一组值
                            name_ = sub_item['modelexcessids'][0]['sublist'][0]['name']
                            value_ = sub_item['modelexcessids'][0]['sublist'][0]['value']
                            if value_ == '●':
                                value_ = '(标配)'
                            if value_ == '○':
                                value_ = '(选配)'
                            value = value_ + str(name_)
                        elif len(sub_item['modelexcessids'][0]['sublist']) > 1:  # 多组值
                            val_dict = list()
                            for ele in sub_item['modelexcessids'][0]['sublist']:
                                name_ = ele['name']
                                value_ = ele['value']
                                if value_ == '●':
                                    value_ = '(标配)'
                                if value_ == '○':
                                    value_ = '(选配)'
                                value_ = value_ + str(name_)
                                val_dict.append(value_)
                            value = val_dict
                        else:
                            value = '-'
                param_of_this_type[name] = value
            if item_type == '基本参数':
                item['base_param'] = param_of_this_type
            elif item_type == '车身':
                item['car_body'] = param_of_this_type
            elif item_type == '发动机':
                item['engine'] = param_of_this_type
            elif item_type == '变速箱':
                item['gear_box'] = param_of_this_type
            elif item_type == '底盘转向':
                item['chassis_trans'] = param_of_this_type
            elif item_type == '车轮制动':
                item['wheel_brake'] = param_of_this_type
            elif item_type == '电动机':
                item['electromotor'] = param_of_this_type

        for sub_param in param_1:
            item_type = sub_param['itemtype']
            param_of_this_type = dict()
            for sub_item in sub_param['items']:
                name = sub_item['name']
                if name == '车内PM2.5过滤装置':  # 特殊处理，字典的key中不能含有‘.’
                    name = '车内细颗粒物过滤装置'
                value = sub_item['modelexcessids'][0]['value']  # 特殊处理几个符号
                if value == '●':
                    value = '标配'
                if value == '○':
                    value = '选配'
                if value == '-':
                    if 'sublist' in sub_item['modelexcessids'][0].keys():  # 是否有值
                        if len(sub_item['modelexcessids'][0]['sublist']) == 1:
                            name_ = sub_item['modelexcessids'][0]['sublist'][0]['name']
                            value_ = sub_item['modelexcessids'][0]['sublist'][0]['value']
                            if value_ == '●':
                                value_ = '(标配)'
                            if value_ == '○':
                                value_ = '(选配)'
                            value = value_ + str(name_)
                        elif len(sub_item['modelexcessids'][0]['sublist']) > 1:  # 多组值
                            val_dict = list()
                            for ele in sub_item['modelexcessids'][0]['sublist']:
                                name_ = ele['name']
                                value_ = ele['value']
                                if value_ == '●':
                                    value_ = '(标配)'
                                if value_ == '○':
                                    value_ = '(选配)'
                                value_ = value_ + str(name_)
                                val_dict.append(value_)
                            value = val_dict
                        else:
                            value = '-'
                param_of_this_type[name] = value
            if item_type == '主/被动安全装备':
                item['safe_device'] = param_of_this_type
            elif item_type == '辅助/操控配置':
                item['assist_operate'] = param_of_this_type
            elif item_type == '外部/防盗配置':
                item['guard_theft_device'] = param_of_this_type
            elif item_type == '内部配置':
                item['inner_config'] = param_of_this_type
            elif item_type == '座椅配置':
                item['seat_config'] = param_of_this_type
            elif item_type == '多媒体配置':
                item['multi_media'] = param_of_this_type
            elif item_type == '灯光配置':
                item['lighting'] = param_of_this_type
            elif item_type == '玻璃/后视镜':
                item['mirror'] = param_of_this_type
            elif item_type == '空调/冰箱':
                item['fridge_air_conditioner'] = param_of_this_type

        for sub_param in param_2:
            item_type = sub_param['itemtype']
            param_of_this_type = dict()
            for sub_item in sub_param['items']:
                value = sub_item['modelexcessids'][0]['value']
                if value == '●':
                    value = '标配'
                if value == '○':
                    value = '选配'
                if value == '-':
                    value = '-'
                index = value.find('.')  # dict 的key不能包含 '.'
                if index != -1:
                    value = value.replace('.', '-')
                tip = sub_item['modelexcessids'][0]['tip']
                price_info = sub_item['modelexcessids'][0]['priceinfo']
                param_of_this_type[value] = [tip, price_info]
            if item_type == '选装包':
                item['select_bag'] = param_of_this_type

        return item
