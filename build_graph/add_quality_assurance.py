#!/usr/bin/env python3
# coding: utf-8
# File: add_quality_assurance.py
# Author: hanrd
# Date: 19-03-06

from utils.data_loader import JsonFileLoader, MongoLoader
from utils.neo4j_op import Neo4jOp
from utils import logger
import sys


class QualityAssuranceGraph:
    def __init__(self):
        self.data_list_1 = JsonFileLoader("../data/motorcycle.json").get_data_list()
        # self.data_list_1 = MongoLoader("MotorcycleTypeItem").get_data_list()

    """读取文件"""
    def read_nodes(self):
        print('开始读入数据\n')
        # 共1类节点
        quality_assurance = []  # 整车质保
        rels_motorcycle_assurance = []  # 车型-质保关系
        data_list_1 = self.data_list_1
        print('motorcycle信息条目：' + str(len(data_list_1)) + '\n')
        for elem in data_list_1:
            motor = elem['series_name'] + ' ' + elem['motorcycle_type_name']
            if 'base_param' in elem.keys():
                if '整车质保' in elem['base_param'].keys():
                    if elem['base_param']['整车质保'] not in quality_assurance:
                        quality_assurance.append(elem['base_param']['整车质保'])
                    rels_motorcycle_assurance.append([motor, elem['base_param']['整车质保']])
        return quality_assurance, rels_motorcycle_assurance

    def create_graphnodes(self):
        print('开始创建实体类型节点\n')
        quality_assurance, rels_motorcycle_assurance = self.read_nodes()
        neo = Neo4jOp()
        neo.create_node('Quality_assurance', quality_assurance)
        print('Quality_assurance nodes have ' + str(len(quality_assurance)) + '\n')
        print('节点类型创建完毕')
        return

    def create_graphrels(self):
        print('开始创建')
        quality_assurance, rels_motorcycle_assurance = self.read_nodes()
        neo = Neo4jOp()
        neo.create_relationship('Motorcycle', 'Quality_assurance', rels_motorcycle_assurance, 'assurance_is',
                                '整车质保是')
        print('关系创建完毕')
        return

    '''导出数据'''
    def export_data(self):
        print('开始导出数据')
        quality_assurance, rels_motorcycle_assurance = self.read_nodes()
        f = open('../dict/quality_assurance.txt', 'w+', encoding='utf-8')
        f.seek(0)
        f.truncate()  # 清空文件
        f.write('\n'.join(list(quality_assurance)))

        f.close()


if __name__ == '__main__':
    sys.stdout = logger.Logger() 
    handler = QualityAssuranceGraph()
    handler.create_graphnodes()
    handler.create_graphrels()
    handler.export_data()
