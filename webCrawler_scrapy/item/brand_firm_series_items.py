# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BrandFirmSeriesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    brand_id = scrapy.Field()
    brand_name = scrapy.Field()
    on_sale_list = scrapy.Field()
    halt_sale_list = scrapy.Field()
    for_sale_list = scrapy.Field()
