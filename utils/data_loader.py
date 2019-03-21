#!/usr/bin/env python3
# coding: utf-8
# File: data_loader.py
# Author: hanrd
# Date: 19-03-05
import json
import pymongo


class JsonFileLoader:
    def __init__(self, file_name):
        self.file_name = file_name

    def get_data_list(self):
        with open(self.file_name, 'r', encoding='utf-8') as file:
            data_json = json.load(file)
        return data_json


class MongoLoader:
    def __init__(self, col_name):
        self.mongo_uri = 'localhost'
        self.mongo_db = 'AutoHome'
        self.col_name = col_name

    def get_data_list(self):
        client = pymongo.MongoClient(self.mongo_uri)
        db = client[self.mongo_db]
        name = self.col_name
        data_list = db[name].find()  # .pretty()
        client.close()
        return data_list
