# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MotorcycleTypeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    brand_id = scrapy.Field()  # 品牌id
    brand_name = scrapy.Field()  # 品牌名
    series_id = scrapy.Field()  # 车系id
    series_name = scrapy.Field()  # 车系名
    level_id = scrapy.Field()  # 级别id
    level_name = scrapy.Field()  # 级别名
    series_tags = scrapy.Field()  # 车系标签
    category = scrapy.Field()  # 车型分类
    on_sale = scrapy.Field()  # 是否在售
    motorcycle_type_id = scrapy.Field()  # 车型id
    motorcycle_type_name = scrapy.Field()  # 车型名
    recom_price = scrapy.Field()  # 推荐指导价格
    description = scrapy.Field()  # 车型描述
    base_param = scrapy.Field()  # 基本参数
    car_body = scrapy.Field()  # 车身
    engine = scrapy.Field()  # 发动机
    electromotor = scrapy.Field()  # 电动机
    gear_box = scrapy.Field()  # 变速箱
    chassis_trans = scrapy.Field()  # 底盘转向
    wheel_brake = scrapy.Field()  # 车轮制动
    safe_device = scrapy.Field()  # 主/被动安全装置
    assist_operate = scrapy.Field()  # 辅助/操控配置
    guard_theft_device = scrapy.Field()  # 外部/防盗配置
    inner_config = scrapy.Field()  # 内部配置
    seat_config = scrapy.Field()  # 座椅配置
    multi_media = scrapy.Field()  # 多媒体配置
    lighting = scrapy.Field()  # 灯光配置
    mirror = scrapy.Field()  # 玻璃/后视镜
    fridge_air_conditioner = scrapy.Field()  # 空调/冰箱
    select_bag = scrapy.Field()  # 选装包
