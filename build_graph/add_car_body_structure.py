#!/usr/bin/env python3
# coding: utf-8
# File: add_car_body_structure.py
# Author: hanrd
# Date: 19-03-05

from utils.data_loader import JsonFileLoader, MongoLoader
from utils.neo4j_op import Neo4jOp
from utils import logger
import sys


class StructureGraph:
    def __init__(self):
        self.data_list_1 = JsonFileLoader("../data/motorcycle.json").get_data_list()
        # self.data_list_1 = MongoLoader("MotorcycleTypeItem").get_data_list()

    """读取文件"""
    def read_nodes(self):
        print('开始读入数据\n')
        # 共1类节点
        car_body_structures = []  # 车身结构
        rels_motorcycle_structure = []  # 车型-车身结构关系
        data_list_1 = self.data_list_1
        print('motorcycle信息条目：' + str(len(data_list_1)) + '\n')
        for elem in data_list_1:
            motor = elem['series_name'] + ' ' + elem['motorcycle_type_name']
            if 'base_param' in elem.keys():
                if '车身结构' in elem['base_param'].keys():
                    if elem['base_param']['车身结构'] not in car_body_structures:
                        car_body_structures.append(elem['base_param']['车身结构'])
                    rels_motorcycle_structure.append([motor, elem['base_param']['车身结构']])
        return car_body_structures, rels_motorcycle_structure

    def create_graphnodes(self):
        print('开始创建实体类型节点\n')
        car_body_structures, rels_motorcycle_structure = self.read_nodes()
        neo = Neo4jOp()
        neo.create_node('Car_Body_Structure', car_body_structures)
        print('Car_Body_Structure nodes have ' + str(len(car_body_structures)) + '\n')
        print('节点类型创建完毕')
        return

    def create_graphrels(self):
        print('开始创建')
        car_body_structures, rels_motorcycle_structure = self.read_nodes()
        neo = Neo4jOp()
        neo.create_relationship('Motorcycle', 'Car_Body_Structure', rels_motorcycle_structure, 'car_structure_is',
                                '车身结构是')
        print('关系创建完毕')
        return

    '''导出数据'''
    def export_data(self):
        print('开始导出数据')
        car_body_structures, rels_motorcycle_structure = self.read_nodes()
        f = open('../dict/car_structure.txt', 'w+', encoding='utf-8')
        f.seek(0)
        f.truncate()  # 清空文件
        f.write('\n'.join(list(car_body_structures)))

        f.close()


if __name__ == '__main__':
    sys.stdout = logger.Logger()
    handler = StructureGraph()
    handler.create_graphnodes()
    handler.create_graphrels()
    handler.export_data()
