# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.utils.project import get_project_settings
import pymysql
import openpyxl
import pymongo
from scrapy import log


class WebCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class ScrapyMongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = item.__class__.__name__
        self.db[collection_name].insert(dict(item))
        return item


class ScrapyMySQLPipeline(object):
    def __init__(self):
        self.settings = get_project_settings()
        self.host = self.settings['MYSQL_HOST']
        self.port = self.settings['MYSQL_PORT']
        self.user = self.settings['MYSQL_USER']
        self.passwd = self.settings['MYSQL_PASSWD']
        self.db = self.settings['MYSQL_DBNAME']
        # 连接数据库
        self.connect = pymysql.connect(host=self.host, db=self.db, user=self.user, passwd=self.passwd, charset='utf8',
                                       use_unicode=False, port=self.port)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            sql, params = item.distinct_data()
            self.cursor.execute(sql, params)
            data = self.cursor.fetchone()
            if data:
                pass
            else:
                # 插入数据
                sql, params = item.get_insert_sql()
                self.cursor.execute(sql, params)
                self.connect.commit()

        except Exception as error:
            # 出现错误时打印错误日志
            log(error)
        return item


class ExcelBossPipeline(object):
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.append(['koubei_id', 'viewcount', 'commentcount', 'helpfulcount', 'update_time'])  # 口碑阅读数

    def process_item(self, item, spider):
        line = [item['koubei_id'], item['visit_count'], item['comment_count'], item["helpful_count"], item['time']]
        self.ws.append(line)
        self.wb.save('../data/口碑历史记录.xlsx')  # 保存xlsx文件
        return item
