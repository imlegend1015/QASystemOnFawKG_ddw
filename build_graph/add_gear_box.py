#!/usr/bin/env python3
# coding: utf-8
# File: add_gear_box.py
# Author: hanrd
# Date: 19-03-06

from utils.data_loader import JsonFileLoader, MongoLoader
from utils.neo4j_op import Neo4jOp
from utils import logger
import sys


class GearBoxGraph:
    def __init__(self):
        self.data_list_1 = JsonFileLoader("../data/motorcycle.json").get_data_list()
        # self.data_list_1 = MongoLoader("MotorcycleTypeItem").get_data_list()

    """读取文件"""
    def read_nodes(self):
        print('开始读入数据\n')
        # 共1类节点
        gear_box = []  # 变速箱
        rels_motorcycle_gear_box = []  # 车型-变速箱关系
        args = []
        arg_dict = dict()
        data_list_1 = self.data_list_1
        print('motorcycle信息条目：' + str(len(data_list_1)) + '\n')
        for elem in data_list_1:
            motor = elem['series_name'] + ' ' + elem['motorcycle_type_name']
            if 'gear_box' in elem.keys():
                if '简称' in elem['gear_box'].keys():
                    if elem['gear_box']['简称'] not in gear_box:
                        gear_box.append(elem['gear_box']['简称'])
                        for key in elem['gear_box'].keys():
                            if key != '简称':
                                arg_dict[key] = elem['gear_box'][key]
                        args.append(arg_dict)
                        arg_dict = dict()
                    rels_motorcycle_gear_box.append([motor, elem['gear_box']['简称']])

        return gear_box, rels_motorcycle_gear_box, args

    def create_graphnodes(self):
        print('开始创建实体类型节点\n')
        gear_box, rels_motorcycle_gear_box, args = self.read_nodes()
        neo = Neo4jOp()
        neo.create_node('Gear_box', gear_box, args)
        print('Gear_box nodes have ' + str(len(gear_box)) + '\n')
        print('节点类型创建完毕')
        return

    def create_graphrels(self):
        print('开始创建')
        gear_box, rels_motorcycle_gear_box, args = self.read_nodes()
        neo = Neo4jOp()
        neo.create_relationship('Motorcycle', 'Gear_box', rels_motorcycle_gear_box, 'gear_box_is',
                                '变速箱是')
        print('关系创建完毕')
        return

    '''导出数据'''
    def export_data(self):
        print('开始导出数据')
        gear_box, rels_motorcycle_gear_box, args = self.read_nodes()
        f = open('../dict/gear_box.txt', 'w+', encoding='utf-8')
        f.seek(0)
        f.truncate()  # 清空文件
        f.write('\n'.join(list(gear_box)))

        f.close()


if __name__ == '__main__':
    sys.stdout = logger.Logger()
    handler = GearBoxGraph()
    handler.create_graphnodes()
    handler.create_graphrels()
    handler.export_data()
